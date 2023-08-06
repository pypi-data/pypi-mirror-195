"""
Data

This is an object that represents the Data area on Lancium Compute.
"""
from distutils.log import error
import os
import json
from math import ceil
from time import sleep
from lancium.core.ApiResource import ApiResource
from lancium.errors.auth import *
from lancium.errors.common import *
from lancium.errors.data import *
from lancium.errors.upload import *

class Data():
    base_url = 'data'
    resource = ApiResource(transaction=None)

    def error_handle(res, path=None, byte_range_start = 0, byte_range_end=-1, url=None, source_type=None, source=None, code = None, error_handling = True, key = None, recurse_count = 0):
        '''Helper Method -- Handles status checking for server response objects. No need to call directly.
        
        ARGS:
        * `res (response object)`: response object from the server
        * `path (string)`: path with the data area
        * `byte_range_start (int, optional)`: byte range start of the expected data 
        * `byte_range_end (int, optional)`: byte range end of the expected data
        * `url (string, optional)`: url to do an API call to the server with
        * `source_type (string, optional)`: type in (file, directory, data, data_recursive, url)
        * `source (string, optional)`: source to retrieve data from (name of file for source_type 'file')

        RETURNS:
            Nothing unless the request is a status code 422 in which case it returns list with the server response
            and a boolean stating that it is a directory.

        '''
        if error_handling:
            is_directory = False
            if res.status_code == 416:
                raise InvalidByteRangeError(
                    "An invalid byte range (%d, %d) was "
                    "specified." %
                    (byte_range_start, byte_range_end))
                
            elif (res.status_code == 422 or res.headers.get('X-Object-Type') == 'directory') and recurse_count==0 and url:
                res = ApiResource.session.get(url)
                Data.error_handle(res, path=path, byte_range_start=byte_range_start, byte_range_end=byte_range_end, url=url, source_type=source_type, source=source, code=None, error_handling=True, key=None, recurse_count=recurse_count+1)
                is_directory = True
                return [res, is_directory]
            elif res.status_code == 403:
                raise ForbiddenDataError(
                    "Requested path '%s' is forbidden." % path)
            elif res.status_code == 400:
                try:
                    errors = res.json()['errors']
                except:
                    raise InternalError(
                        "Received a '400' response code but no 'error' element received in server response.")
                raise BadDataRequestError(message=errors)
            elif res.status_code == 409:
                raise DataConflictError(
                    "Requested path '%s' already exists." % path)
            elif res.status_code == 503:
                raise UnavailableDataError(
                    "Data at '%s' is temporarily unavailable." % path)
            elif source_type in {'data','data_recursive'} and res.status_code == 404:
                raise ResourceNotFoundError(
                    "Requested source data path '%s' does not exist." % source)
            elif source_type == 'data' and res.status_code == 422:
                raise PathIsDirectoryError(
                    "Requested source data path '%s' is a directory." %
                    path)
            elif res.status_code == 411:
                raise MissingContentLength('Content-Length header not included in request.')
            elif res.status_code == 412:
                raise FileChecksumMismatch('Checksum Mismatch.')
            
        if code != None and res!=None:
            ApiResource._verify_response(res=res, code=code, key=key)

    def _verify_session_and_input(path, **kwargs):
        """Verifies session, input path, and set the request API Key.

        Args:
        * `path (string)`: path in data area
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")

        if not path:
            raise InvalidInputError("Invalid Data path provided.")
        
        if kwargs:
            if Data.resource.session.key != kwargs.get('auth') and kwargs.get('auth'):
                Data.resource.setter(key=kwargs.get('auth'))

    @staticmethod
    def create(path,
               source_type,
               source=None,
               force=False, **kwargs):
        """Create a new data object.

        **POST /data/<path>**
        

        Args:
        * `path (string)`: path in Lancium’s persistent storage area
        * `source_type (string)`: type of Data (‘file’, ‘url’)
        * `source (string)`: local path (source_type: file, url (source_type: url)
        * `force (bool)`: forces data upload even if path already exists within the persistent storage
        * `**kwargs(dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        Returns: 
            Data (lancium.api.Data): Data object

        ```python
        import os
        from lancium.api.Data import Data

        def fake_callback(total_chunks, current_chunk):
            pass

        data = Data().create('test1', 'file', source = os.path.abspath('impish.simg'), force=True)
        data.upload( os.path.abspath('impish.simg'),fake_callback)
        print(data.__dict__)

        ###OUTPUT BELOW
        {'_Data__key': None, 'path': 'test1', 'is_dir': False, 'length': None, 'last_modified': None, 'date_created': None}
        ```
        """
        if not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        Data._verify_session_and_input(path, **kwargs)

        if not source_type:
            raise InvalidInputError("Invalid source type provided.")

        if source_type not in {
                'file',
                'directory',
                'data',
                'data_recursive',
                'url'}:
            raise InvalidInputError(
                "Invalid source type '%s' provided." % source_type)

        if source_type in ['data', 'file', 'url','data_recursive'] and not source:
            raise InvalidInputError(
                "A source must be provided for the '%s' type." % source_type)

        url = ApiResource.build_url(Data.base_url)

        payload = {}
        payload['source_type'] = source_type
        if source:
            if source_type == 'file':
                payload['source'] = os.path.basename(source)
            else:
                payload['source'] = source
        if source_type == 'file':
            payload['size'] = os.path.getsize(os.path.abspath(source))

        payload['path'] = path
        payload['force'] = force

        res = ApiResource.session.post(url, data=json.dumps(payload))
        
        Data.error_handle(res=res, path=path, source=source, source_type=source_type, url=url, code=202)

        is_dir = True if source_type == 'directory' or source_type == 'data_recursive' else False
        data = Data(path=path, is_dir = is_dir, **kwargs)
        return data

    def refresh(self):
        """Refresh metadata about a specific file or get contents of a directory.

        **HEAD /data/<path> if file**

        **GET /data/<path> if directory**

        Args:
            None

        Returns:
            None (None): None

        ```python
        import os
        from lancium.api.Data import Data

        def fake_callback(total_chunks, current_chunk):
            pass

        data = Data.create('testing_path', 'file', os.path.abspath('asd.py'), True)
        data.upload('asd.py', fake_callback)
        print(data.is_dir)
        data.is_dir = True
        print(data.is_dir)
        data.refresh()
        print(data.is_dir)

        ###OUTPUT BELOW
        False
        True
        False

        ```
        """
        if not self.__dict__.get('_Data__key') or not self.__key:
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Data.resource.setter(key=self.__key)
        Data._verify_session_and_input(self.path)

        url = Data.resource.build_url(Data.base_url, self.path)
        res = Data.resource.session.head(url)

        is_directory = False

        returned = Data.error_handle(res=res, url=url, path=self.path)
        if returned:
            res, is_directory = returned[0], returned[1]


        if is_directory:
            Data.error_handle(res=res, code=200, key='contents', error_handling=False)
            self.is_dir = True
        else:
            Data.error_handle(res=res, code=204, error_handling=False)

        attr = {}
        attr['is_dir'] = is_directory
        attr['length'] = res.headers.get('X-File-Size')
        attr['last-modified'] = res.headers.get('X-Last-Modified')
        attr['date-created'] = res.headers.get('X-Date-Created')
        self.__dict__.update(**attr)

    @staticmethod
    def get(path, byte_range_start=0, byte_range_end=-
            1, download_path=None, callback=None, **kwargs):
        """Get a Data object by path.

        **GET /data/<path>**

        Args:
        * `path (string)`: path in Lancium’s persistent storage area
        * `byte_range_start (int, optional)`: starting byte for Data if downloading data file
        * `byte_range_end (int, optional)`: ending byte for Data if downloading data file
        * `download_path (string, optional)`: location to save data from the persistent storage area
        * `callback (func, optional)`: called after each chunk is downloaded, accepts arguments in the form of (download stage, percent complete, current_chunk_contents)
        * `**kwargs (dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}
        Returns:
            Data (lancium.api.Data): a Data object
        
        ```python
        ### PRINT IT OUT
        import os
        from time import sleep
        from lancium.api.Data import Data


        def desk(stage, progress, contents): 
            if contents != None:
                print(type(contents))
                contents = str(contents)
                contents = contents [2:-1]
                print(contents)
                
        def fake_callback(total_chunks, current_chunk):
            pass

        data = Data().create('test1', 'file', source = os.path.abspath('impish.simg'), force=True)
        data.upload(os.path.abspath('impish.simg'),fake_callback)
        sleep(5)
        ex1 = Data.get('test1', callback = desk)
        ### OUTPUT BELOW FROM ABOVE CODE

        <class 'bytes'>
        'Bootstrap: docker\nFrom: ubuntu:bionic\n\n%runscript\napt-get update \n'

        ### DOWNLOAD IT (NEW CODE)
        import os
        from time import sleep
        from lancium.api.Data import Data

                
        def fake_callback(total_chunks, current_chunk):
            pass

        data = Data().create('test1', 'file', source = os.path.abspath('impish.simg'), force=True)
        data.upload(os.path.abspath('impish.simg'),fake_callback)
        sleep(5)
        ex1 = Data.get('test1', download_path='./')
        os.system('ls test1')   

        ###OUTPUT BELOW
        test1
        ```
        """
        if not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        Data._verify_session_and_input(path, **kwargs)
        
        url = ApiResource.build_url(Data.base_url, path)
        is_dir = False

        if download_path:
            if not os.access(download_path, os.W_OK):
                raise InvalidInputError(
                    "Specified download path is not writable.")

            filename = os.path.basename(path)
            out_path = os.path.join(download_path, filename)
            raw_file = open(out_path, 'wb')

        headers = {}
        if byte_range_start < 0:
            raise InvalidByteRangeError(
                "Start of byte range cannot be negative.")

        if byte_range_end >= 0:
            if byte_range_start > byte_range_end:
                raise InvalidByteRangeError("Start of byte range cannot be "
                                            "after end of byte range.")
            headers['range'] = 'bytes=%d-%d' % (
                byte_range_start, byte_range_end)
        res = ApiResource.session.get(url, headers=headers, stream=True)
        Data.error_handle(res, path=path,url=url, byte_range_start=byte_range_start, byte_range_end=byte_range_end)
        while res.status_code == 202 :
            output = res.json()
            if callback:
                callback('preparing', output['progress'], None)
            sleep(5)
            res = ApiResource.session.get(url, headers=headers, stream=True)

        if res.headers.get('X-Object-Type') == 'directory':
            is_dir = True

        if 'range' in headers:
            Data.error_handle(res=res, code=206, error_handling=False)
        else:
            Data.error_handle(res=res, code=200, error_handling=False)

        if download_path and is_dir == True:
            raise PathIsDirectoryError("Cannot download directories. '%s' is a directory." % path)
        
        if not is_dir:
            current_chunk = 0
            file_size = int(res.headers.get('Content-Length'))
            total_chunks = ceil(float(file_size) / ApiResource.CHUNK_SIZE)

            if callback:
                callback('downloading', (current_chunk/total_chunks)*100, None)

            for chunk in res.iter_content(ApiResource.CHUNK_SIZE):
                if download_path:
                    raw_file.write(chunk)

                if callback:
                    current_chunk += 1
                    callback('downloading', (current_chunk/total_chunks)*100, chunk)
            '''
            for chunk in res.iter_content(ApiResource.CHUNK_SIZE):
                if download_path:
                    raw_file.write(chunk)

                if callback:
                    current_chunk += 1
                    callback('downloading', (current_chunk/total_chunks)*100, chunk)
            '''

        if download_path:
            raw_file.close()

        attrs = res.headers
        new_data = Data(path=path, is_dir = is_dir)
        new_data.__dict__.update(**attrs)
        return new_data

    @staticmethod
    def show(path, **kwargs):
        """Retrieve metadata about a specific file or get contents of a directory.

        **HEAD /data/<path> if file**

        **GET /data/<path> if directory**

        Args:
        * `path (string)`: path within the persistent data area.
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        Returns:
            list of Data objects: a list of Data of objects

        ```python
        import os
        from lancium.api.Data import Data

        def fake_callback(total_chunks, current_chunk):
            pass

        Data().create('test1', 'file', source = os.path.abspath('impish.simg'), force=True)
        Data().upload('test1', os.path.abspath('impish.simg'),fake_callback)

        ex1 = Data.show('test1')[0]

        print(ex1)

        ### OUTPUT BELOW
        {'_Data__key': None, 'path': 'test1', 'is_dir': False, 'length': '66', 'last_modified': 'Thu, 13 Oct 2022 18:39:42 +0000', 'date_created': 'Thu, 13 Oct 2022 18:39:42 +0000'}


        ```
        
        """
        if not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        Data._verify_session_and_input(path, **kwargs)

        url = ApiResource.build_url(Data.base_url,path)
        res = ApiResource.session.head(url)

        is_directory = False

        returned = Data.error_handle(res=res, path=path, url=url)
        if returned and isinstance(returned, list):
            res, is_directory = returned[0], returned[1]

        if is_directory:
            Data.error_handle(res=res, code=200, key='contents', error_handling=False)
            children = Data.flatten_children_to_arr(path=path, contents=res.json()['contents'])
            return children
        else:
            Data.error_handle(res=res, code=204, error_handling=False)
            attr = {}
            attr['X-File-Size'] = res.headers['X-File-Size']
            attr['X-Last-Modified'] = res.headers['X-Last-Modified']
            attr['X-Date-Created'] = res.headers['X-Date-Created']
            return [Data(path=path, is_dir=False, **attr)]

    def children(self):
        '''Retrieves the file / directory children of a directory object
        
        **HEAD data/<path>/**

        **GET data/<path>/**

        Args:
            None

        Returns: 
            (list of lancium.api.Data): array of Data objects

        ```python
        from lancium.api.Data import Data

        folder = Data.get('test2')

        print(f"folder is Directory? {folder.is_dir}")

        children = folder.children()

        print(f"this is folder's children: {children}")

        ###OUTPUT BELOW
        folder is Directory? True
        this is folder's children: [<lancium.api.Data.Data object at 0x7fd0274591b0>, ... ,<lancium.api.Data.Data object at 0x7fd027b37d60>]

        ```
        '''
        if not self.__dict__.get('_Data__key') or not self.__key:
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Data.resource.setter(key=self.__key)
            
        if self.is_dir == False:
            raise InvalidInputError('Children can only be called on a directory.')

        url = ApiResource.build_url(Data.base_url, self.path + '/')
        res = Data.resource.session.head(url)
        returned = Data.error_handle(res=res, path=self.path, url=url)
        if returned and isinstance(returned, list):
            res, is_directory = returned[0], returned[1]

        Data.error_handle(res=res, code=200, key='contents', error_handling=False)
        children = Data.flatten_children_to_arr(path=self.path, contents=res.json()['contents'])
        return children

    def flatten_children_to_arr(path, contents):
        '''Flattens data objects to arrays.

        Args:
        * `contents (json)`: contents of the response json object.

        Returns:
            array of Data objects
        '''
        children = []
        for dict in contents:
            attrs = {'X-File-Size': dict.get('size'), 
                    'X-Last-Modified': dict.get('last_modified'), 
                    'X-Date-Created': dict.get('created')}
            # append data object to array of children
            children.append(Data(path=path + '/' + dict.get('name') if path != '/' else dict.get('name'), is_dir=dict.get('is_directory'), **attrs))
        return children

    def upload(self, file_path, callback=None):
        """Upload file.

        **PATCH /data/<path>**

        Args:
        * `file_path (string)`: local file path of input file
        * `callback (func, optional)`: called after each chunk is downloaded, accepts arguments in the form of (file_size, file_start, total_chunks, current_chunk)

        Returns:
            response (Requests.response): response object in json format

        ```python
        import os
        from lancium.api.Data import Data

        def fake_callback(total_chunks, current_chunk):
            pass

        data = Data().create('test1', 'file', source = os.path.abspath('impish.simg'), force=True)
        data.upload(os.path.abspath('impish.simg'),fake_callback)

        ex = data.show('test1')[0]
        print(ex.__dict__)

        ###OUTPUT BELOW
        {'_Data__key': None, 'path': 'test1', 'is_dir': False, 'length': '66', 'last_modified': 'Thu, 13 Oct 2022 18:41:00 +0000', 'date_created': 'Thu, 13 Oct 2022 18:41:00 +0000'}

        ```
        
        """
        if not self.__dict__.get('_Data__key') or not self.__key:
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Data.resource.setter(key=self.__key)
        Data._verify_session_and_input(self.path)
        if not file_path or not os.path.isfile(file_path):
            raise InvalidInputError("Invalid Data file path provided.")

        url = ApiResource.build_url(Data.base_url, self.path)
        res = ApiResource.handle_upload(url, file_path, callback)
        Data.error_handle(res=res, code=201, path = file_path)

        data = res.json()
        if 'upload_complete' not in data or not data['upload_complete']:
            raise InternalError("Upload failed.")
        return data
    
    @staticmethod
    def delete(path, recursive = False, **kwargs):
        """Delete data object (file or directory)

        **DELETE /data/<path>**

        ARGS:
        * `path (string)`: path in Data area
        * `recursive (boolean)`: flag for whether to delete recursive (directory)
        * `**kwargs (dictionary)`: contains key 'auth' optionally to state which api key to use
        
        RETURNS:
            None: None

        ```python
        from lancium.api.Data import Data


        Data().delete('test1')
        Data().show('test1')

        ###OUTPUT BELOW
        The requested resource could not be found.

        ```  
        """
        if not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        Data._verify_session_and_input(path, **kwargs)

        url = ApiResource.build_url(Data.base_url, path)
        if recursive:
            url += '?recursive=true'
        res = ApiResource.session.delete(url)
        if res.status_code == 409:
            raise DirectoryNotEmptyError("Specified directory is not empty.")
        Data.error_handle(res=res, code=202, error_handling=False)
    
    def destroy(self, recursive=False):
        """Delete data object.

        **DELETE /data/<path>**

        ARGS:
        * `recursive (boolean)`: flag for whether to delete recursive (directory)
        
        RETURNS:
            None: None

        ```python
        from lancium.api.Data import Data

        folder = Data.get('test2')

        print(folder.path != None)

        folder.destroy(recursive=True)

        print(folder.path != None)

        ###OUTPUT BELOW
        True
        False
        ```
        """
        if not self.__dict__.get('_Data__key') or not self.__key:
            Data.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Data.resource.setter(key=self.__key)
        Data.delete(path=self.path, recursive=recursive)

        for key in self.__dict__.keys():
            self.__dict__[str(key)] = None #need this, otherwise dict changes size during iteration

    def __init__(self, path=None, is_dir = False, **kwargs):
        """
        ARGS:
        * `path (string)`: path in the persistent storage area
        * `is_dir (bool)`: Boolean for whether data object is a directory
        * `length (int)`: length of Data object in bytes
        * `last_modified (string)`: last modified date and time of Data object
        * `date_created (string)`: date and time of Data object creation
        * `__key (string)`: auth key
        """
        if kwargs.get('transaction'):
            Data.resource.set_transaction(transaction=kwargs.get('transaction'))
        self.__key = self.__dict__.get('_Data__key')
        if kwargs.get('auth') and not self.__key:
            self.__key = kwargs.get('auth')
            self.resource.setter(key=kwargs.get('auth'))
        if not self.resource.session:
            raise MissingCredentialsError("Missing credentials.")
        self.path = path
        self.is_dir = is_dir
        self.length = kwargs.get('X-File-Size')
        self.last_modified = kwargs.get('X-Last-Modified')
        self.date_created = kwargs.get('X-Date-Created')