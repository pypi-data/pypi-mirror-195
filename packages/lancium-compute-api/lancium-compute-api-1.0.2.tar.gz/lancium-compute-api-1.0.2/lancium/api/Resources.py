"""
Resources

This is an object that retieves resources provided by Lancium Compute.
"""
from lancium.core.ApiResource import ApiResource
from lancium.errors.auth import *
from lancium.errors.common import *
import os


class Resources():
    base_url = 'resources'
    resource = ApiResource(transaction=None)
    def resource_helper(type, to_check):
        '''
        Helper method for the static methods. Retrieves
        requested information.
        '''
        if type == 'all':
            url = ApiResource.build_url(Resources.base_url)
        else:
            url = ApiResource.build_url(Resources.base_url,type)
        res = ApiResource.session.get(url)
        ApiResource._verify_response(res, 200)

        data = res.json()
        if to_check in data:
            return data[to_check]
        else:
            raise InternalError(f'No {to_check} element received in server response.')
    
    def session_checker(**kwargs):
        if Resources.resource.session.key != kwargs.get('auth') and kwargs.get('auth') and kwargs.get('auth'):
            Resources.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Resources.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        if not ApiResource.session:
            raise MissingCredentialsError('Missing credentials.')

    @staticmethod
    def all(**kwargs):
        """Retrieves a list of available resource types.

        **GET /resources**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different acocunt {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of available resources
        """
        Resources.session_checker(**kwargs)
        return Resources.resource_helper('all', 'resources')

    @staticmethod
    def gpus(**kwargs):
        """Retrieves a list of available GPUs.

        **GET /resources/gpus**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different acocunt {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of available GPUs
        """
        Resources.session_checker(**kwargs)
        return Resources.resource_helper('gpus', 'gpus')

    @staticmethod
    def mpi(**kwargs):
        """Retrieves a list of support MPI implementations.

        **GET /resources/mpi**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different acocunt {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of supported implementations
        """
        Resources.session_checker(**kwargs)
        return Resources.resource_helper('mpi', 'mpi_versions')

    @staticmethod
    def qos(**kwargs):
        """Retrieves a list of available qos levels.

        **GET /resources/qos**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different acocunt {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of available levels
        """
        Resources.session_checker(**kwargs)
        return Resources.resource_helper('qos', 'qos')

    @staticmethod
    def defaults(**kwargs):
        """Retrieves a list of default job resource values.

        **GET /resources/defaults**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different acocunt {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of defaults
        """
        Resources.session_checker(**kwargs)
        return Resources.resource_helper('defaults', 'defaults')

    @staticmethod
    def limits(**kwargs):
        """Retrieves a list of default job resource limits.

        **GET /resources/limits**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different acocunt {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of limits
        """
        Resources.session_checker(**kwargs)
        return Resources.resource_helper('limits', 'limits')

    def __init__(self, **kwargs):
        '''This is an object that represent gets the resources of Lancium Compute.
        
        PARAMETERS:
        * `__key`: api key

        '''
        if kwargs.get('transaction'):
            Resources.resource.set_transaction(transaction=kwargs.get('transaction'))
        self.__key = self.__dict__.get('_Resources__key')
        if kwargs.get('auth') and not self.__key:
            self.__key = kwargs.get('auth')
            self.resource.setter(key=kwargs.get('auth'))
        if not self.resource.session:
            raise MissingCredentialsError("Missing credentials.")

