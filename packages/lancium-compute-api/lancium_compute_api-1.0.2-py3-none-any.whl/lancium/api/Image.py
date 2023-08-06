"""
Image

This is an object that represents a computational environment. Used to create a
Singularity container.
"""
from distutils.log import error
import os
import json
from lancium.core.ApiResource import ApiResource
from lancium.errors.auth import *
from lancium.errors.common import *
from lancium.errors.image import *


class Image(object):
    base_url = 'images'
    resource = ApiResource(transaction=None)

    def error_handle(res=None, name=None, data=None, error_handling=True, code=None, key=None):
        '''Helper Method -- Handles status checking for server response objects 

        ARGS:
        * `res (response object)`: response object from the server
        * `name (string)`: Image name
        * `data (json)`: json of payload for the api call
        * `code (int)`: status code to check for
        * `error_handling (boolean)`: flag for whether to do internal handling
        * `key ('str')`: key for response object

        RETURNS:
            Nothing unless the request is a status code 422 in which case it returns list with the server response
            and a boolean stating that it is a directory.

        '''        
        if error_handling:
            if res.status_code == 400:
                    try:
                        errors = res.json()['errors']
                    except:
                        raise InternalError(
                            "Received a '400' response code but no 'error' element received in server response.")
                    raise ImageValidationError(name=name, message=errors)
            elif res.status_code == 403:
                    raise ForbiddenNamespaceError('No permission on requested path.')
            elif data and ('upload_complete' not in data or not data['upload_complete']):
                raise InternalError("Upload failed.")
            elif res.status_code == 409:
                raise ImageRebuildError("Can't rebuild an image that is already building.")
            
        if code != None and res:
            ApiResource._verify_response(res=res, code=code, key=key) 
    
    def input_validation(source_type=None, build_script=None, source=None, source_url=None):
        '''Helper Method -- Handles argument checking
        
        ARGS:
        * `source_type (string)`: Image type (singularity_image, singularity_file, docker_image, docker_file)
        * `source_url (string)`: url to source file
        * `source (string)`: path to source file
        * `build_script (string)`: path to the build script for a singularity_file or docker_file

        RETURNS:
            Nothing.

        '''    
        if source_type and source_type not in {'docker_image', 'docker_file', 'singularity_image', 'singularity_file'}:
            raise InvalidInputError("Invalid Image source type provided. "
                                    "Can be one of 'docker_image', "
                                    "'docker_file', 'singularity_image', "
                                    "or 'singularity_file'.")

        if build_script and source_type not in {'singularity_file', 'docker_file'}:
            raise InvalidInputError(
                f"Cannot specify 'build_script' field with source type {source_type}.")

        if source and source_type not in {'singularity_image', 'docker_image'}:
            raise InvalidInputError(
                f"Cannot specify 'source' field with source type {source_type}.")

        if source_url and source_type not in {'singularity_image', 'docker_image'}:
            raise InvalidInputError(
                f"Cannot specify 'source_url' field with source type {source_type}.")

        if source and source_url:
            raise InvalidInputError(
                "Cannot specify both 'source' and 'source_url' fields.")

    @staticmethod
    def all(**kwargs):
        """Retrieve all Images.

        **GET /images**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of Images
        
        ```python
        from lancium.api.Image import Image

        imgs = Image().all()
        print(imgs)


        ### OUTPUT BELOW
        '[<lancium.api.Image.Image object at 0x7f737491e8c0>,..., <lancium.api.Image.Image object at 0x7f737491f430>]'

        ```
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Image.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        url = ApiResource.build_url(Image.base_url)
        res = ApiResource.session.get(url)
        Image.error_handle(res=res, code=200)

        data = res.json()
        if 'images' in data:
            result = []
            for img in data['images']:
                if not img.get('_Image__key'):
                    img['auth'] = kwargs.get('auth')
                result.append(Image(img.pop('path'), name=img.pop('name'), **img ))
            return result
        elif 'image' in data:
            data = res.json()['image']
            if not data.get('_Image__key'):
                data['auth'] = kwargs.get('auth')
            return [Image(name=data.pop('name'), path=data.pop('path'), **data)]
        else:
            raise InternalError("No 'images' element received "
                                "in server response.")

    @staticmethod
    def create(path, name, source_type, **kwargs):
        """Create a new image.

        **POST /images**

        Args:
        * `path (string)`: Image path
        * `name (string)`: Image name
        * `description (string)`: description of image
        * `Source_type (string)`: Image type [docker_file, docker_image, singularity_image, singularity_file)
        * `source_url (string)`: url ot source file
        * `source (string)`: path to source image file
        * `build_script (string)` : path to build script for docker_file and singualrity_file
        * `environment (list of dict)`: environment variables to be added to image
        * `kwargs(dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        Returns:
            Image: Image object
        

        ```python
        import os
        from lancium.api.Image import Image

        with open(os.path.abspath('pythonDocker.txt')) as build_script:
            contents = build_script.read()
        params = {'build_script': contents}
        imgs = Image().create(path='testing123', name='testing123', source_type='docker_file',**params)

        ### IMAGE OUTPUT BELOW

        [
            {
                "path": "testing123",
                "name": "testing123",
                "source_type": "docker_file",
                "build_script": "contents of build-script",
                "status": "building",
                "created_at": "2022-07-07T16:53:37.237Z",
                "updated_at": "2022-07-07T16:53:39.000Z"
            }
        ]


        ```
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Image.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        build_script = kwargs.get('build_script')
        source = kwargs.get('source')
        source_url = kwargs.get('source_url')
        description = kwargs.get('description')
        environment = kwargs.get('environment')

        if not path:
            raise InvalidInputError("Invalid Image path provided.")
        if not name:
            raise InvalidInputError("Invalid Image name provided.")
        Image.input_validation( source_type=source_type, source=source, build_script=build_script, source_url=source_url)

        url = ApiResource.build_url(Image.base_url)

        payload = {}
        payload['path'] = path
        payload['name'] = name
        payload['source_type'] = source_type

        if description:
            payload['description'] = description
        if source:
            payload['size'] = os.path.getsize(source)
        if source_url:
            payload['source_url'] = source_url
        if build_script:
            payload['build_script'] = build_script
        if environment:
            payload['environment'] = environment

        res = ApiResource.session.post(url, data=json.dumps(payload))

        Image.error_handle(res=res, name=name, code=201)
        payload['auth'] = kwargs.get('auth')
        return Image(path=payload.pop('path'), name=payload.pop('name'), **payload )

    @staticmethod
    def get(path, **kwargs):
        """Retrieve specific image(s) by path.

        **GET /images/<path>**

        Args:
        * `path (string)`: path to image(s)
        * `kwargs (dictionary)`: can contain auth to perform this method using a different account. ('auth': ANOTHER_API_KEY)

        Return:
            list: list of Images
        
        ```python
        from lancium.api.Image import Image

        imgs = Image().get('testing123')
        print(imgs[0].path)
        print(imgs[0].name)
        print(imgs[0].source_type)

        ### OUTPUT BELOW
        'testing123'
        'testing123'
        'docker_file'

        ```
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Image.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        if not path:
            raise InvalidInputError("Invalid Image path provided.")

        url = ApiResource.build_url(Image.base_url, path)
        res = ApiResource.session.get(url)
        Image.error_handle(res=res, code=200)
        if 'image' in res.json():
            data = res.json()['image']
            if not data.get('_Image__key'):
                data['auth'] = kwargs.get('auth')
            return [Image(name=data.pop('name'), path=data.pop('path'), **data)]
        elif 'images' in res.json():
            data = res.json()['images']
            result = []
            for img in data:
                if not img.get('_Image__key'):
                    img['auth'] = kwargs.get('auth')
                result.append(Image(name=img.pop('name'), path=img.pop('path'), **img))
            return result
        else:
            raise InternalError("No 'image' or 'images' element received "
                                "in server response.")

    def update(self, **kwargs):
        """Updates an existing image.

       **PUT /images/<path>**

        ARGS:
        * `path (string)`: Image path
        * `name (string)`: Image name
        * `description (string)`: description of image
        * `source_type (string)`: Image type [docker_file, docker_image, singularity_image, singularity_file)
        * `source_url (string)`: url ot source file
        * `source (string)`: path to source image file
        * `buidl_script (string)` : path to build script for docker_file and singualrity_file
        * `environment (list of dict)`: environment variables to be added to image
        
        RETURNS:
            None: None

        ```python
        from lancium.api.Image import Image

        imgs = Image().get('testing123')
        testing123 = imgs[0]
        update = {'name': 'testing321'}
        testing123.update(**update)
        imgs2 = Image().get('testing123')
        print(imgs2[0].name)

        ### OUTPUT BELOW
        'testing321'

        ```
        """
        if not self.__dict__.get('_Image__key') or not self.__key:
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Image.resource.setter(key=self.__key)

        source_type = kwargs.get('source_type')
        source_url = kwargs.get('source_url')
        source = kwargs.get('source')
        build_script = kwargs.get('build_script')


        Image.input_validation(source_type=source_type, build_script=build_script, source=source, source_url=source_url)

        url = ApiResource.build_url(Image.base_url,self.path)
        res = self.resource.session.put(url, data=json.dumps(kwargs))

        Image.error_handle(res=res, code=200, key='image')

        data = res.json()['image']
        del data['path']
        self.name = data['name']
        del data['name']
        self.__dict__.update(data)

    def refresh(self):
        """Refresh a specific image to reflect database.

        **GET /images/<path>**

        Args:
            None (None)
        
        RETURNS:
            None: None

        ```python
        from lancium.api.Image import Image
        from lancium.errors.common import *


        img = Image.get('ubuntu')[0]

        img.name = 'not_ubuntu'

        print(img.name)

        img.refresh()

        print(img.name)

        ###OUTPUT BELOW
        not ubuntu
        ubuntu
        ```
        """
        if not self.__dict__.get('_Image__key') or not self.__key:
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Image.resource.setter(key=self.__key)
        url = ApiResource.build_url(Image.base_url, self.path)
        res = self.resource.session.get(url)
        Image.error_handle(res=res, code=200)

        # Clear any previous attributes
        for key in self.__dict__.keys():
            if key != 'path':
                self.__dict__[key] = None

        if 'image' in res.json():
            data = res.json()['image']
            del data['path']
            self.name = data['name']
            del data['name']
            self.__dict__.update(data)
        elif 'images' in res.json():
            raise InvalidInputError("Provided path includes multiple images.")
        else:
            raise InternalError("No 'image' or 'images' element received "
                                "in server response.")

    def upload(self, file_path, callback=None):
        """Upload image.

        **PATCH /images/<path>**

        Args:
        * `file_path (string)`: file to upload
        * `callback (func, optional)`: called after each chunk is successfully uploaded, accepts arguments in the format of (file_size, file_start, total chunks, current chunk)

        Returns:
            Response object: response object in json format
        """
        if not self.__dict__.get('_Image__key') or not self.__key:
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Image.resource.setter(key=self.__key)

        if not file_path or not os.path.isfile(file_path):
            raise InvalidInputError("Invalid Image file path provided.")

        url = self.resource.build_url(Image.base_url, self.path)
        res = self.resource.handle_upload(url, file_path, callback)
        Image.error_handle(res=res, code=201, error_handling=False)

        data = res.json()
        if 'upload_complete' not in data or not data['upload_complete']:
            raise InternalError("Upload failed.")
        return data

    def rebuild(self):
        """Rebuild existing image.

        **POST /images/<path>/rebuild**

        ARGS:
            None (None)
        
        RETURNS:
            None: None
        
        ```python
        from lancium.api.Image import Image

        imgs = Image().get('testing123')
        testing321 = imgs[0]
        testing321.rebuild()

        ### IMAGE BELOW
        [
            {
                "path": "testing123",
                "name": "testing123",
                "source_type": "docker_file",
                "build_script": "build script",
                "status": "building",
                "created_at": "2022-07-07T16:53:37.237Z",
                "updated_at": "2022-07-07T18:26:37.541Z",
                "built_at": "2022-07-07T17:08:51.243Z"
            }
        ]


        ```
        """
        if not self.__dict__.get('_Image__key') or not self.__key:
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Image.resource.setter(key=self.__key)
        url = self.resource.build_url(Image.base_url, self.path, 'rebuild')
        res = self.resource.session.post(url)
        Image.error_handle(res=res, code=202)

    @staticmethod
    def delete(path, **kwargs):
        """Delete image.

        **DELETE /images/<path>**

        ARGS:
        * `path (string)`: path to image object within Lancium
        * `kwargs (dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}
        
        RETURNS:
            None: None  

        ```python
        from lancium.api.Image import Image
        from lancium.errors.common import *


        Image.delete('test/mlperf2')

        try:
            Image.get('test/mlperf2')
        except:
            print('not found')

        ### OUTPUT BELOW
        not found

        ```
        """
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Image.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
            
        url = ApiResource.build_url(Image.base_url, path)
        res = ApiResource.session.delete(url)
        Image.error_handle(res=res, code=202, error_handling=False)

    def destroy(self):
        '''
        Delete current image

        **DELETE /images/<self>**

        Args:
            None (None)

        Returns:
            None: None

        ```python
        from lancium.api.Image import Image
        from lancium.errors.common import *


        img = Image.get('zzzz')[0]

        img.destroy()

        try:
            Image.get('zzzz')
        except:
            print('not found')

        ###OUTPUT BELOW
        not found
        ```
        '''
        if not self.__dict__.get('_Image__key') or not self.__key:
            Image.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Image.resource.setter(key=self.__key)
        Image.delete(self.path, **{'auth': self.__key})

        #destroy locally
        attrs = self.__dict__
        for key in attrs.keys():
            attrs[key] = None
        self.name = None
        self.path = None


    def __init__(self, path=None, name=None, **kwargs):
        """Initialize an Image object.

        ARGS:
        * `path (string)`: Image path
        * `name (string)`: Image name
        * `description` (string): description of job
        * `source_type` (string): Image type
        * `source_url` (string): url to source of Image
        * `source` (string): path to source file
        * `build_script` (string): build script for data
        * `environment` (list of dict): environment variables to be added to image
        * `status` (string): status of Image
        """
        if kwargs.get('transaction'):
            Image.resource.set_transaction(transaction=kwargs.get('transaction'))
        self.__key = self.__dict__.get('_Image__key')
        if kwargs.get('auth') and not self.__key:
            self.__key = kwargs.get('auth')
            self.resource.setter(key=kwargs.get('auth'))
        if not self.resource.session:
            raise MissingCredentialsError("Missing credentials.")

        self.path = path
        self.name = name
        self.description = kwargs.get('description')
        self.source_type = kwargs.get('source_type')
        self.source_url = kwargs.get('source_url')
        self.source = kwargs.get('source')
        self.build_script = kwargs.get('build_script')
        self.environment = kwargs.get('environment', None)
        self.status = kwargs.get('status')
