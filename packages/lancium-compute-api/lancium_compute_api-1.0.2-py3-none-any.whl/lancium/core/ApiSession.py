"""
ApiResource

Base class for all API requests. Provides the session used to make requests.

Attributes:
    key: API key
    access_token: Temporary ccess token
    no_cache: Flag to disable cache
    CACHE_PATH: Cache file path where the API key and access token are stored
"""

import os
import configparser
import jwt
import time
import warnings
import sys
import collections 
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping

from requests import Session
from requests.adapters import HTTPAdapter
from tests.adapters.MockApiAdapter import MockApiAdapter
from lancium.errors.auth import *

API_ROOT = os.getenv('LANCIUM_API_ROOT', 'https://portal.lancium.com/api/v1')


class ApiSession():

    VERSION = '1.6.0'
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(
            self,
            key=None,
            access_token=None,
            no_cache=False,
            cache_path=None,
            transaction=None,
    ):
        """Initializes ApiSession object.

        Initializes ApiSession object using provided or cached credentials.
        Mounts an API adapter depending on the current environment.

        Args:
            key (string)
            access_token (string)
            no_cache (boolean, optional): flag for caching credentials. Defaults to False.
            cache_path (string, optional)
        """
        self.CACHE_PATH = cache_path
        self.CACHE_FLAG = not no_cache
        self.keys = {}
        self.key = key
        self.access_token = access_token

        self.session = Session()
        env = os.getenv('LANCIUM_ENV', 'PRODUCTION')
        

        if env == 'TEST':
            self.session.mount('https://', MockApiAdapter())
            self.key = os.getenv("LANCIUM_API_KEY", "foobar")
            global API_ROOT
            API_ROOT = 'https://localhost'
        else:
            self.session.mount('https://', HTTPAdapter())

        if transaction:
            self.session.headers.update(
                {'X-Transaction-ID': transaction}
            )
        
        if not key or not access_token:
            self._retrieve_credentials()
        else:
            self._cache_credentials()

        self.refresh_access_token()
        self.keys = {self.key: self.access_token}

    def mount_test(self):
        self.key = os.getenv("LANCIUM_API_KEY", "foobar")
        self.session.mount('https://', MockApiAdapter())
        global API_ROOT
        API_ROOT = 'https://localhost'       

    def _update_headers(self, access_token = None):
        """Update request headers.

        Modifies request headers to use the current access token.
        """
        self.session.headers.update(
            {'Authorization': 'Bearer {}'.format(self.access_token if not access_token else access_token)})
        if access_token:
            self.access_token = access_token

    ##################################
    #   Credentials
    ##################################

    def refresh_access_token(self, key = None):
        """Verifies that the access token is still valid. Generates a new
        token if the current one has expired.
        """
        if not self._verify_access_token(key):
            self._fetch_access_token()
        if not key:
            self._update_headers()

    def _verify_access_token(self, key=None):
        """Verify access token is valid.

        Returns:
            bool: True if the token is still valid. False if invalid.
        """
        try:
            if key:
                return True
            payload = jwt.decode(self.access_token, options={"verify_signature": False})
            return (int(time.time())+3600) <= payload['exp']
        except jwt.exceptions.InvalidTokenError:
            return False

    def _fetch_access_token(self):
        """Retreives a new access token.

        Modifies headers to use the API key instead of an access token. Issues
        a request to

            POST /access_tokens
        """
        self.access_token = self.keys.get(self.key)
        if self.access_token and self._verify_access_token(self.key):
            return

        url = os.path.join(API_ROOT, 'access_tokens')
        self.session.headers.update(
            {'Authorization': 'Bearer {}'.format(self.key)})
        
        res = self.session.post(url)
        if res.status_code != 201:
            raise InvalidCredentialsError("Invalid API key provided.")

        if not self.key:
            self.access_token = res.headers['Authorization'].split(' ')[1]
        else:
            access_token = res.headers['Authorization'].split(' ')[1]

        if not self.key:
            self._cache_credentials()
        self._update_headers() if not self.key else self._update_headers(access_token)

    def _cache_credentials(self):
        """Saves credentials to CACHE_PATH.
        """
        if self.CACHE_FLAG and self.CACHE_PATH:
            if not os.getenv('LANCIUM_API_KEY') or os.getenv('LANCIUM_API_KEY') == self.key:
                config = configparser.ConfigParser()
                config['AUTH'] = {'api_key': self.key or '',
                                'access_token': self.access_token or ''}
                with open(self.CACHE_PATH, 'w') as configfile:
                    config.write(configfile)
                os.chmod(os.path.dirname(self.CACHE_PATH), 0o700)
                os.chmod(self.CACHE_PATH, 0o600)

    def _retrieve_credentials(self, key=None):
        """Retrieves credentials from CACHE_PATH.

        if no credentials are provided (or no key), both key and access token
        will be retrieved from the cache.

        If a key is provided without an access token, the access token will be
        attempted to be found.
        """
        if self.CACHE_PATH:
            try:
                config = configparser.ConfigParser()
                config.read(self.CACHE_PATH)
                auth = config['AUTH']

                if (self.key == auth['api_key']) or not self.key:
                    self.key = auth['api_key']

                    if not self.access_token or not self.key:
                        self.access_token = auth['access_token']
            except BaseException:
                pass

        if not self.key:
            raise MissingCredentialsError("Could not find a valid API key.")

    ##################################
    #   Overrides
    ##################################

    def request(self, verb, url, timeout, *args, **kwargs):
        """Performs extra checks and does data processing before request.
        """
        self.refresh_access_token(key = kwargs.get('key'))
        request_url = os.path.join(API_ROOT, url)
        res = verb(request_url, *args, **kwargs, timeout=timeout)
        if(res.headers.get('X-Deprecated-API-Used') and res.headers.get('X-Deprecated-API-Used') == 'true'):
            warnings.warn("Using a deprecated major API version", DeprecationWarning)
        if(res.headers.get('X-Current-API-Version') and res.headers.get('X-Current-API-Version') != ApiSession.VERSION):
            warnings.warn("Using an outdated version of this library", FutureWarning)
        return res

    def get(self, *args, **kwargs):
        """Override get method in Session.
        """
        self.session.headers.pop('Content-Type', None)
        return self.request(self.session.get, timeout=(90,300), *args, **kwargs)

    def head(self, *args, **kwargs):
        """Override head method in Session.
        """
        self.session.headers.pop('Content-Type', None)
        return self.request(self.session.head, timeout=(90,300), *args, **kwargs)

    def post(self, *args, **kwargs):
        """Override post method in Session.
        """
        self.session.headers.update({'Content-Type': 'application/json'})
        return self.request(self.session.post,  timeout=(90,300), *args, **kwargs)

    def put(self, *args, **kwargs):
        """Override put method in Session.
        """
        self.session.headers.update({'Content-Type': 'application/json'})
        return self.request(self.session.put, timeout=(90,300), *args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete method in Session.
        """
        self.session.headers.pop('Content-Type', None)
        return self.request(self.session.delete, timeout=(90,300), *args, **kwargs)

    def patch(self, *args, **kwargs):
        """Override patch method in Session.
        """
        self.session.headers.update(
            {'Content-Type': 'application/octet-stream'})
        return self.request(self.session.patch,timeout=(90,600), *args, **kwargs)
