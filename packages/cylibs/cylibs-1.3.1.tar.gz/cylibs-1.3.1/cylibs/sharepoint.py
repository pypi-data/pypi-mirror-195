import os
import requests
import logging

from requests_ntlm import HttpNtlmAuth
from xml.etree import ElementTree


class SharePoint:
    # reference: https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest
    def __init__(self, server, site, user, pwd, debug=False, verify_ssl=False):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.propagate = debug  # propagate log to higher level

        self.server = server
        self.site = site
        self.user = user
        self.pwd = pwd
        self.auth = HttpNtlmAuth(self.user, self.pwd)
        self.verify_ssl = verify_ssl

        if not verify_ssl:
            requests.packages.urllib3.disable_warnings()

    def retry(times):
        def decorator_retry(func):
            def wrapper_retry(*args, **kwargs):
                print("wrapper_retry")
                for i in range(times):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        print(f"Retry: {i+1}/{times}, Error: {e}")
                raise Exception("All retry failed!")
            return wrapper_retry
        return decorator_retry

    # list file or folder
    def _list_by_type(self, folder, list_folder=False):
        list_type = "Folders" if list_folder else "Files"
        url = f"{self.server}/{self.site}/_api/web/GetFolderByServerRelativeUrl('/{self.site}/{folder}')/{list_type}"
        self.log.debug(f"url={url}")
        ret = []
        response = requests.get(url, auth=self.auth, verify=self.verify_ssl)
        if response.status_code != 200:
            raise Exception("Error response={}".format(response.text))
        tree = ElementTree.fromstring(response.content)
        for entry in tree.iter(tag='{http://www.w3.org/2005/Atom}entry'):
            for content in entry.iter(tag='{http://www.w3.org/2005/Atom}content'):
                for property in content.iter(
                        tag='{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
                    for name in property.iter(tag='{http://schemas.microsoft.com/ado/2007/08/dataservices}Name'):
                        ret.append(name.text)
        self.log.debug(f"ret={ret}")

        return ret

    def list(self, folder, recursive=False):
        ret = self._list_by_type(folder)

        if recursive:
            folders = self._list_by_type(folder, list_folder=True)
            for f in folders:
                files_in_f = self.list(f"{folder}/{f}", recursive=True)
                for i in files_in_f:
                    ret.append(f"{f}/{i}")

        return ret

    def delete(self, file):
        url = self.server + '/' + self.site + "/_api/web/GetFileByServerRelativeUrl('/" + self.site + '/' + file + "')"
        self.log.debug("url=%s", url)

        # get digest first
        response = requests.post(url, auth=self.auth, verify=self.verify_ssl)
        digest = response.headers['X-RequestDigest']

        headers = {
            'If-Match': "*",
            'X-HTTP-Method': "DELETE",
            'X-RequestDigest': digest,
        }
        response = requests.post(url, auth=self.auth, headers=headers, verify=self.verify_ssl)
        if response.status_code != 200:
            raise Exception("Error response={}".format(response.text))

    @retry(5)
    def download(self, file, target_file):
        url = self.server + '/' + self.site + '/' + file

        response = requests.get(url, stream=True, auth=self.auth, verify=self.verify_ssl)
        if response.status_code != 200:
            raise Exception("Error response={}".format(response.text))
        with open(target_file, 'wb') as f:
            f.write(response.content)

    @retry(5)
    def upload(self, folder, file):
        file_name = os.path.basename(file)

        url = self.server + '/' + self.site + \
            "/_api/web/GetFolderByServerRelativeUrl('/" + self.site + '/' + \
            folder + "')/Files/Add(url='" + file_name + "', overwrite=true)"
        self.log.debug("url=%s", url)

        # get digest first
        response = requests.post(url, auth=self.auth, verify=self.verify_ssl)
        digest = response.headers['X-RequestDigest']

        with open(file, 'rb') as f:
            data = f.read()
            headers = {
                'Content-Length': str(len(data)),
                'X-RequestDigest': digest,
            }
            response = requests.post(url, auth=self.auth, headers=headers, data=data, verify=self.verify_ssl)
            if response.status_code != 200:
                raise Exception("Error response={}".format(response.text))
