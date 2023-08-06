"""
ApiResource

Base class for all API resources. Provides helper functions used to make requests.

Attributes:
    CHUNK_SIZE: File upload size in bytes
    RETRY_LIMIT: Number of times an upload request will be attempted
"""

import threading
import os
from time import sleep
from hashlib import md5
from math import ceil
from lancium.core.ApiSession import ApiSession
from lancium.errors.auth import *
from lancium.errors.common import *
from lancium.errors.data import NoContentError, PartialContentError
from lancium.errors.upload import *


class ApiResource():
    CHUNK_SIZE = 10000000

    __instance = None
    session = None
    _lock = threading.Lock()

    def __new__(cls, path = None, name = None, transaction = None, *args, **kwargs):
        if cls.__instance is None:
            with cls._lock:
                if cls.__instance is None:
                    cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, transaction, *args, **kwargs):
        """Initialize an ApiResource.

        Args:
            session (ApiSession)
        """
        self.CACHE_PATH = os.environ.get('LANCIUM_CACHE_PATH', kwargs.get('cache_path'))

        if kwargs.get('auth'):
            key = kwargs.get('auth')
        else:
            key = os.environ.get('LANCIUM_API_KEY')

        if self.CACHE_PATH:
            cache_dir, filename = os.path.split(
                os.path.expanduser(self.CACHE_PATH))
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)
            if not os.access(cache_dir, os.W_OK):
                raise InvalidInputError(
                    "Cannot write to specified cache path.")
        else:
            cache_dir = os.path.expanduser('~/.lancium')
            filename = 'lancium.conf'
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)
            if not os.access(cache_dir, os.W_OK):
                cache_dir = os.path.dirname(os.path.abspath(__file__))
            self.CACHE_PATH = os.path.join(cache_dir, 'lancium.conf')
        self.transaction = transaction
        ApiResource.session = ApiSession(key, None, False, self.CACHE_PATH, transaction)
    
    def setter(self, key):
        self.session.key = key
        self.session._fetch_access_token()
    
    def set_transaction(self, transaction):
        self.transaction = transaction
        self.session.session.headers.update(
                {'X-Transaction-ID': transaction}
            )

    @staticmethod
    def _verify_response( res, code, key=None):
        """Checks for the correct HTTP response code, and
        throws the appropriate exception if the response
        code does not match, or an invalid server response
        is received.

        Args:
            res (HttpResponse): HTTP response to request
            code (int): expected HTTP response code
            key (string, optional): expected dictonary key to check
        """
        if res.status_code == 401:
            raise InvalidCredentialsError("Invalid API key provided.")

        if res.status_code == 404:
            raise ResourceNotFoundError(
                "The requested resource could not be found.")

        if res.status_code == 200 and code != 200:
            raise InternalError('Response was unexpectedly successful.')
        if res.status_code == 202 and code != 202:
            raise LanciumError('Download is still preparing.')
        
        if res.status_code == 204 and code != 204:
            raise NoContentError('No Content.')
        
        if res.status_code == 206 and code != 206:
            raise PartialContentError('Parital content received.')


        if res.status_code != code:
            raise LanciumError(
                "Received unexpected response code of '%d' from server." %
                res.status_code)

        if key:
            if key not in res.json():
                raise InternalError(
                    "No '%s' element received in server response." % key)

    @staticmethod
    def build_url(base_url, *args):
        """Constructs request url.

        Args:
            *args: list of url path components

        Returns:
            string: request path relative to API root
        """
        parts = []
        for arg in args:
            part = str(arg)
            if part == '/' or part == '':
                continue
            if part[0] == '/':
                parts.append(part[1:])
            else:
                parts.append(part)
        return os.path.join(base_url, *parts)

    @staticmethod
    def build_file_upload_header(
            content_length,
            upload_offset,
            upload_checksum=None):
        """Constructs header for patch requests.

        Constructs header with required fields to upload files.

        Args:
            content_length (int): number of bytes in the body
            upload_offset (int): number of bytes already uploaded
            upload_checksum (Base64): MD5 checksum for the chunk

        Returns:
            dict: request header
        """
        headers = {
            'Content-Length': str(content_length),
            'Upload-Offset': str(upload_offset),
        }

        if upload_checksum:
            headers['Upload-Checksum'] = upload_checksum

        return headers

    @staticmethod
    def handle_upload(url, upload_path, callback=None, retry=5):
        """Handles file uploads.

        Uploads file through chunks of configured size to the server. Can automatically
        retry if an upload fails.

        Args:
            url (string)
            upload_path (string): file location
            callback (func, optional): called after each chunk is successfully uploaded,
                            accepts arguments in the format of (file_size,
                            file_start, total_chunks, current_chunk)
            retry (int, optional): maximum number of times to retry if the upload fails


        Returns:
            res (Response): Response object from the last chunk uploaded
        """
        file_size = os.path.getsize(upload_path)
        if file_size == 0:
            raise InvalidInputError("Uploading an empty file is unsupported.")
        res = None

        with open(upload_path, 'rb') as obj:
            file_start = 0

            total_chunks = ceil(
                float(file_size) / ApiResource.CHUNK_SIZE)  # 32 MB
            current_chunk = 0

            callback(current_chunk, total_chunks)

            while current_chunk < total_chunks:
                file_end = min(file_size, file_start + ApiResource.CHUNK_SIZE)

                obj.seek(file_start)
                data = obj.read(ApiResource.CHUNK_SIZE)
                checksum = md5(data).hexdigest()

                headers = ApiResource.build_file_upload_header(
                    ApiResource.CHUNK_SIZE, file_start, checksum)

                attempts = 0
                while attempts < retry:  # Upload chunk
                    try:
                        attempts += 1
                        res = ApiResource.session.patch(
                            url, headers=headers, data=data)

                        if res.status_code == 404:
                            raise ResourceNotFoundError(
                                "Upload resource not found.")
                        elif res.status_code == 409:
                            raise FileCompleteConflict(
                                "File upload already completed.")
                        elif res.status_code == 412:
                            raise FileChecksumMismatch(
                                "File checksum mismatch.")
                        elif res.status_code == 411:
                            raise MissingContentLength(
                                "Content length missing.")

                        res.raise_for_status()
                        break
                    except Exception as e:
                        if not retry:
                            raise e
                            break
                        elif attempts < retry:
                            sleep(0.5)
                        else:
                            raise e
                            break

                file_start = file_end
                current_chunk += 1
                callback(current_chunk, total_chunks)

        return res

    @staticmethod
    def handle_download(url, download_path=None, callback=None):
        """Handles file downloads.

        Downloads file through chunks of configured size from the server.

        Args:
            url (string)
            download_path (string, optional): location to download file to
            callback (func, optional): called after each chunk is successfully downloaded,
                            accepts arguments in the format of (download stage, percent complete, current_chunk_contents)


        Returns:
            res (Response): Response object from the last chunk downloaded
        """

        if download_path:
            if not os.access(download_path, os.W_OK):
                raise InvalidInputError(
                    "Specified download path is not writable.")

            filename = os.path.basename(url)
            out_path = os.path.join(download_path, filename)
            raw_file = open(out_path, 'wb')

        res = ApiResource.session.get(url, stream=True)

        # If we get back a 204, the file was blank, so just return to the caller

        if res.status_code == 204:
            return res

        # If we get back a 202, the download is still being staged to the API server
        # check back in 5 seconds

        while res.status_code == 202 :
            output = res.json()
            if callback:
                callback('preparing', output['progress'], None)
            sleep(5)
            res = ApiResource.session.get(url, stream=True)

        ApiResource._verify_response(res, 200)

        current_chunk = 0

        file_size = int(res.headers['Content-Length'])
        total_chunks = ceil(float(file_size) / ApiResource.CHUNK_SIZE)

        if callback:
            callback('downloading', (current_chunk/total_chunks)*100, None)

        for chunk in res.iter_content(ApiResource.CHUNK_SIZE):
            if download_path:
                raw_file.write(chunk)
            if callback:
                current_chunk += 1
                callback('downloading', (current_chunk/total_chunks)*100, chunk)

        if download_path:
            raw_file.close()

        return res
