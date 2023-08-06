"""
JobInput

This is an object that represents job input data.
"""
import os
from lancium.core.ApiResource import ApiResource
from lancium.errors.common import *
from lancium.errors.auth import *
from lancium.errors.job import *
from lancium.errors.upload import *


class JobInput():
    base_url = 'jobs'
    resource = ApiResource(transaction=None)
    def upload(self, file_path, callback=None):
        """Upload input data for a job.

        **PATCH /jobs/<id>/data/<data-id>**

        Args:
        * `file_path (string): file path of input file
        * `callback (func)`: called after each chunk is successfully uploaded, accepts arguments in the format of (file_size, file_start, total_chunks, current_chunk)

        Returns:
            JSON: Response Object in JSON format
        """
        if not self.__dict__.get('_JobInput__key') or not self.__key:
            JobInput.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            JobInput.resource.setter(key=self.__key)
        if not file_path or not os.path.isfile(file_path):
            raise InvalidInputError("Invalid Job input file path provided.")

        url = self.resource.build_url(JobInput.base_url, self.job_id, 'data', self.id)
        res = self.resource.handle_upload(url, file_path, callback)

        if res.status_code == 409:
            raise JobAlreadySubmittedError(
                "Cannot update an already submitted Job.")
        elif res.status_code == 411:
            raise MissingContentLength('Content-Length header not included in request.')
        elif res.status_code == 412:
            raise FileChecksumMismatch('Checksum Mismatch.')
        elif res.status_code == 422:
            raise FileUploadError(f'Unable to upload the specified source type {self.source_type}.')

        self.resource._verify_response(res, 201)

        data = res.json()
        if not data['upload_complete']:
            raise InternalError("Upload failed.")
        return data
    
    @staticmethod
    def delete(job_id, id, **kwargs):
        """Delete input data from a job.

        **DELETE /jobs/<id>/data/<data-id>**

        ARGS:
        * `job_id (int)`: Job ID
        * `id (int)`: JobInput ID
        
        Returns: 
            None: None
        """
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            JobInput.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            JobInput.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        url = ApiResource.build_url(JobInput.base_url, job_id, 'data', id)
        res = ApiResource.session.delete(url)
        if res.status_code == 409:
            raise JobAlreadySubmittedError(
                "Cannot update an already submitted Job.")
        ApiResource._verify_response(res, 202)

    def destroy(self):
        """Delete input data from a job.

        **DELETE /jobs/<id>/data/<data-id>**

        ARGS:
            None (None)
        
        Returns: 
            None: None
        """
        if not self.__dict__.get('_JobInput__key') or not self.__key:
            JobInput.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            JobInput.resource.setter(key=self.__key)
        JobInput.delete(self.job_id, self.id)

        # Destroy locally
        attrs = self.__dict__
        for key in attrs.keys():
            attrs[key] = None
        self.id = None
        self.job_id = None

    """
    Object methods
    """

    def __init__(self, id, job_id, **kwargs):
        """Initialize a JobInput object.

        Args:
        * `id (int)`: unique identifier for JobInput (data-id)
        * `job_id (int)`: associated Job ID
        * `name (string)`: filename in the job working directory
        * `source_type (string)`: one of these options ('file', 'data', 'url')
        * `source (string)`: source location of the input data
        * `cache (bool, optional)`: if True, the file is copied to the node during
                                execution as READ ONLY
        upload_complete (bool): boolean representing whether the upload has been completed
        chunks_received (string): represents the range of chunks received by Lancium Compute
        """
        if kwargs.get('transaction'):
            JobInput.resource.set_transaction(transaction=kwargs.get('transaction'))
        self.__key = self.__dict__.get('_JobInput__key')
        if kwargs.get('auth') and not self.__key:
            self.__key = kwargs.get('auth')
            self.resource.setter(key=kwargs.get('auth'))
        if not self.resource.session:
            raise MissingCredentialsError("Missing credentials.")
        self.id = id
        self.job_id = job_id
        self.name = kwargs.get('name')
        self.source_type = kwargs.get('source_type')
        self.source = kwargs.get('source')
        self.cache = kwargs.get('cache', False)
        self.upload_complete = kwargs.get('upload_complete', False)
        self.chunks_received = kwargs.get('chunks_received', [])
