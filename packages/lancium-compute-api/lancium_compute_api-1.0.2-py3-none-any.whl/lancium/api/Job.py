"""
Job

This is an object that represents a computational job.
"""
import os
import json
from lancium.core.ApiResource import ApiResource
from lancium.api.JobInput import JobInput
from lancium.errors.auth import *
from lancium.errors.common import *
from lancium.errors.job import *
from time import sleep
from math import ceil

class Job(object):
    base_url = 'jobs'
    resource = ApiResource(transaction=None)

    def error_handle(res=None, data=None, error_handling=True, code=None, key=None):
        '''Helper Method -- Handles status checking for server response objects. Checks for the correct HTTP response code, and
        throws the appropriate exception if the response
        code does not match, or an invalid server response
        is received.
        
        ARGS:
        * `res (response object)`: response object from the server
        * `data (json)`: json of payload for the api call
        * `args (boolean)`: boolean for whether we are argument checking
        * `res (HttpResponse)`: HTTP response to request
        * `code (int)`: expected HTTP response code
        * `key (string, optional)`: expected dictonary key to check

        RETURNS:
            Nothing unless the request is a status code 422 in which case it returns list with the server response
            and a boolean stating that it is a directory.

        ''' 
        if error_handling:
            is_directory = False
            if res.status_code == 400:
                try:
                    errors = res.json()['errors']
                except:
                    raise InternalError(
                        "Received a '400' response code but no 'error' element received in server response.")
                raise JobValidationError(message=errors)
            elif res.status_code == 402:
                # User doesn't have billing info
                raise BillingInfoError(
                    "Account billing information must be present before submitting.")
            elif res.status_code == 403:
                raise ForbiddenDataError('No permissions on requested path.')
            elif res.status_code == 409:
                raise JobAlreadySubmittedError(
                    "Cannot update an already submitted Job.")
            elif res.status_code == 422:
                raise PathIsDirectoryError('Path is a directory and not a file.')
            elif res.status_code == 503:
                # error-free job but cannot run with current qos
                raise QoSUnavailableError(
                    "Requested QoS not available. Try again later or lower specified QoS.")
        if res!= None and code:
            ApiResource._verify_response(res, code, key=key)
            if key:
                if key != 'jobs' and 'id' not in res.json()[key]:
                    raise InternalError(
                        "No 'id' element received in server response.")

    def input_validation(name, source_type, source):
        '''Helper Method -- Handles argument checking
        
        ARGS:
        * `name (string)`: job name
        * `source_type (string)`: job input source_type
        * `source`: job input source

        RETURNS:
            Nothing

        ''' 
        if not name:
            raise InvalidInputError("Invalid Job input filename provided.")
        if source_type not in {'file', 'data', 'url', 'data_recursive'}:
            raise InvalidInputTypeError(
                "Invalid Job input source type provided. "
                "Can be one of 'file', 'data', 'data_recursive' or 'url'.")
        if not source:
            raise InvalidInputError("Invalid Job input source provided.")

    def _populate_job_input(self, id, data, auth=None):
        """Populates response data with JobInput objects.

        Args:
        * `id (int)`: job id
        * `data (dict)`: dictionary representing a Job object
        Returns:
            dict: modified response
        """
        if 'input_files' in data:
            new_input = []
            for input_file in range(len(data['input_files'])):
                data_id = data['input_files'][input_file]['id']
                del data['input_files'][input_file]['id']
                new_input.append(
                    JobInput(data_id, id, **data['input_files'][input_file]))
            data['input_files'] = new_input
        return data

    def _populate_payload(self, **kwargs):
        """Populates payload with provided arguments from kwargs.

        Args:
        * `**kwargs`: Keyword arguments
        Returns:
            dict: populated payload
        """
        payload = {}
        for key, value in kwargs.items():
            if value and key != 'job_id':
                payload[key] = value
        return {'job': payload}

    @staticmethod
    def all(**kwargs):
        """Retrieve all Jobs.

        **GET /jobs**

        ARGS:
        * `**kwargs (dictionary)`: can contain auth key to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        Returns:
            list: list of Jobs

        ```python
        from lancium.api.Job import Job


        all = Job().all()
        print(all)

        ### OUTPUT BELOW
        [<lancium.api.Job.Job object at 0x7f5861683220>,..., <lancium.api.Job.Job object at 0x7f5861681570>]

        ### Recommend flattening each Job to a dictionary of job attributes

        ```
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")
        
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Job.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        url = ApiResource.build_url(Job.base_url)
        res = ApiResource.session.get(url)
        Job.error_handle(res=res, code=200, key='jobs', error_handling=False)

        data = res.json()
        result = []
        for job in data['jobs']:
            if kwargs.get('auth') and not job.get('auth'):
                job['auth'] = kwargs.get('auth')
            result.append(Job(job.pop('id'), **job))
        return result

    @staticmethod
    def create(**kwargs):
        """Create a new Job prior to submission.

        **POST /jobs**

        Args:
        * `name (string)`: job name
        * `notes (string)`: job description
        * `account (string)`: string for internal account billing
        * `qos (string)`: quality of service
        * `command_line (string)`: command line argument
        * `image (string)`: base image for container to run job on
        * `resources (dict)`: dictionary containing the fields 
            * `core_count (int)`
            * `gpu (string)`
            * `vram (int)`
            * `gpu_count (int)` 
            * `memory (int)`
            * `scratch (int)`
        * `max_run_time (int)`: max run time for job (in seconds)
            * `Limit`: 30 days
        * `expected_run_time (int)`: expected run time of job (in seconds)
        * `input_files (list of JobInput)`: input files for Job wrapped in a Job_Input object. 
        * `output_files (tuple)`: expected output file(s) from job
            * Format: (‘output_file1.txt{:name_to_save_as_in_storage.txt}{:archive?}, …)
            * The destination in persistent storage is optional.
        * `callback_url (string)`: Webhook URL to receive updates when job status changes
        * `environment (tuple of strings)`: tuple of environment variables to set for job
            * Format: (‘var1=def1’, ‘var2=def2’,...)
        * `kwargs(dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        Returns:
            Job: Job object

        ```python
        from lancium.api.Job import Job

        params = {'name': 'test', 'command_line': 'ls'}
        job = Job().create(**params)
        print(job.name)
        print(job.command_line)

        ### OUTPUT BELOW
        'test'
        'ls'

        ```
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")

        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Job.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        url = ApiResource.build_url(Job.base_url)
        new_job = Job(**{'auth': kwargs.get('auth')})
        payload = new_job._populate_payload(**kwargs)
        
        res = ApiResource.session.post(url, data=json.dumps(payload))

        Job.error_handle(res=res, code=201, key='job')

        data = res.json()['job']
        id = data.pop('id')
        attr = new_job._populate_job_input(id, data)
        new_job.__dict__.update(**attr)
        new_job.id = id
        return new_job

    @staticmethod
    def get(id, **kwargs):
        """Get a Job object by ID.

        **GET /jobs/<id>**

        Args:
        * `id (int)`: job id
        * `kwargs(dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        RETURNS:
            Job: a Job object

        ```python
        from lancium.api.Job import Job

        params = {'name': 'test', 'command_line': 'ls'}
        job = Job().create(**params)
        id = job.id
        job2 = Job().get(id)
        print(id)
        print(job2.id)

        ### OUTPUT BELOW
        '58317'
        '58317'

        ```
        """
        if not ApiResource.session:
            raise MissingCredentialsError("Missing credentials.")
        if not id:
            raise InvalidInputError("Invalid Job ID provided.")
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Job.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))

        url = ApiResource.build_url(Job.base_url, id)
        res = ApiResource.session.get(url)
        Job.error_handle(res=res, code=200, key='job', error_handling=False)
        data = res.json()['job']
        new_job = Job(id=id, **{'auth': kwargs.get('auth')})
        del data['id']
        attr = new_job._populate_job_input(id, data)
        new_job.__dict__.update(**attr)
        return new_job

    def update(self, **kwargs):
        """Update an existing job if it is not running, errored, or finished (update an existing job if it is in a “created” state.

        **PUT /jobs/<id>**

        Args:
        * `name (string)`: job name
        * `notes (string)`: job description
        * `account (string)`: string for internal account billing
        * `qos (string)`: quality of service
        * `command_line (string)`: command line argument
        * `image (string)`: base image for container to run job on
        * `resources (dict)`: dictionary containing the fields 
            * `core_count (int)`
            * `gpu (string)`
            * `vram (int)`
            * `gpu_count (int)` 
            * `memory (int)`
            * `scratch (int)`
        * `max_run_time (int)`: max run time for job (in seconds)
            * `Limit`: 30 days
        * `expected_run_time (int)`: expected run time of job (in seconds)
        * `input_files (list of JobInput)`: input files for Job wrapped in a Job_Input object. 
        * `output_files (tuple)`: expected output file(s) from job
            * Format: (‘output_file1.txt{:name_to_save_as_in_storage.txt}{:archive?}, …)
            * The destination in persistent storage is optional.
        * `callback_url (string)`: Webhook URL to receive updates when job status changes
        * `environment (tuple of strings)`: tuple of environment variables to set for job
            * Format: (‘var1=def1’, ‘var2=def2’,...)
        * `kwargs(dictionary)`: can contain auth key if you would like to perform this method using a different account. {'auth': ANOTHER_API_KEY}

        RETURNS:
            None: None

        ```python
        from lancium.api.Job import Job

        job = Job().get(58317)
        to_update = {'core_count': 48}
        job.update(**to_update)
        print(job.__dict__)

        ### OUTPUT BELOW
        {'id': 58317, 'name': 'test', 'notes': None, 'account': None, 'status': 'created', 'qos': 'high', 'command_line': 'ls', 'image': None, 'resources': {'core_count': 48, 'gpu_count': None, 'memory': 96, 'gpu': None, 'scratch': None}, 'max_run_time': 259200, 'expected_run_time': None, 'input_files': [], 'output_files': [], 'callback_url': None, 'mpi': None, 'mpi_version': None, 'tasks': None, 'tasks_per_node': None, 'created_at': '2022-07-01T14:00:07.137Z', 'updated_at': '2022-07-01T14:18:30.036Z', 'submitted_at': None, 'completed_at': None}

        ```

        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)

        url = self.resource.build_url(Job.base_url, self.id)
        payload = self._populate_payload(**kwargs)

        res = self.resource.session.put(url, data=json.dumps(payload))

        Job.error_handle(res=res, code=200, key='job')

        data = res.json()['job']
        del data['id']
        attr = self._populate_job_input(self.id, data)
        self.__dict__.update(attr)

    def refresh(self):
        """Refresh attributes of a Job object.
        Overwrites all existing attributes.

        **GET /jobs/<id>**

        ARGS:
            None (None)

        RETURNS:
            None: None

        ```python
        from lancium.api.Job import Job

        kwargs = {'name': 'this is my name', 'image': 'lancium/ubuntu', 'command': 'ls', 'cores': '6', 'mem': '12'}

        job = Job.create(**kwargs)

        print(job.name)
        job.name = 'this is NOT my name'
        print(job.name)

        job.refresh()

        print(job.name)

        ###OUTPUT BELOW
        this is my name
        this is NOT my name
        this is my name
        ```
        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)
        url = self.resource.build_url(Job.base_url, self.id)
        res = self.resource.session.get(url)
        Job.error_handle(res=res, code=200, key='job', error_handling=False)

        for key in self.__dict__:
            if key != 'id':
                self.__dict__[key] = None

        data = res.json()['job']
        del data['id']
        attr = self._populate_job_input(self.id, data)
        self.__dict__.update(attr)

    def submit(self):
        """Submit a job for execution.

        **POST /jobs/<id>/submit**

        ARGS:
            None (None)
        
        RETURNS:
            None: None

        ```python
        from lancium.api.Job import Job

        job = Job().get(58317)
        print(job.status)
        to_update = {'image': 'lancium/ubuntu'}
        job.update(**to_update)
        job.submit()
        job.get(58317)
        print(job.status)

        ### OUTPUT BELOW
        'created'
        'submitted'

        ```
        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)
        url = self.resource.build_url(Job.base_url, self.id, 'submit')
        res = self.resource.session.post(url)

        Job.error_handle(res=res, code=202)

    def output_get(self, file_path, download_path=None, callback=None):
        """Get an output file from a job. If download path is provided, the
        file is saved at the path specified.

        **GET /jobs/<id>/output/<file_path>**

        Args:
        * `file_path (string)`: file path from the job
        * `download_path (string, optional)`: location (directory) to save the file

        Returns:
            res (requests.Response): response object from server

        ```python
        from lancium.api.Job import Job
        import os

        job = Job().get(58317)
        res = job.output_get(file_path='stdout.txt', download_path='.')
        os.system('cat stdout.txt')

        ### OUTPUT BELOW
        'JOBNAME'
        'qsub7683928698168045722.sh'
        'rusage-running.json'
        'stderr.txt'
        'stdout.txt'

        ```
        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)
        if not file_path:
            raise InvalidInputError("Invalid Job output file path provided.")

        url = self.resource.build_url(Job.base_url, self.id, 'output', file_path)
        res = ApiResource.handle_download(url, download_path, callback=callback)
        return res

    def terminate(self):
        """Terminate a running job.

        **POST /jobs/<id>/terminate**

        Args:
            None (None)
        
        Returns:
            None: None

        ```python
        from lancium.api.Job import Job


        params = {'name': 'test', 'command_line': 'sleep(60)', 'image': 'lancium/ubuntu'}
        job = Job().create(**params)
        print(job.id)
        job.submit()

        job.terminate()

        ### OUTPUT BELOW
        99872

        ```
        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)
        url = self.resource.build_url(Job.base_url, self.id, 'terminate')
        res = self.resource.session.post(url)

        Job.error_handle(res=res, code=202)

    def suspend(self):
        """Suspend a running job. NOT IMPLEMENTED, will throw error.

        **POST /jobs/<id>/suspend**
        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)
        url = self.resource.build_url(Job.base_url, self.id, 'suspend')
        res = self.resource.session.post(url)
        Job.error_handle(res=res, code=202, error_handling=False)

    @staticmethod
    def delete(id, **kwargs):
        """Delete a job.

        **DELETE /jobs/<id>**

        Args:
        * `id (int): Job ID`
        
        Returns:
            None: None

        ```python
        # DELETE JOBS WITH ERROR STATUs
        from lancium.api.Job import Job
        from lancium.errors.common import *

        kwargs = {'name': 'This is a test job', 'image': 'lancium/ubuntu', 'command': 'ls', 'notes': 'this is a note'}
        job = Job.create(**kwargs)

        job_id = job.id
        print(job_id)

        Job.delete(job_id)

        try:
            Job.get(job_id)
        except ResourceNotFoundError:
            print('Oh no, the resource was not found.')

        ###OUTPUT BELOW
        94442
        Oh no, the resource was not found.
        ```
        """
        if ApiResource.session.key != kwargs.get('auth') and kwargs.get('auth'):
            Job.resource.setter(key=kwargs.get('auth'))
        elif not kwargs.get('auth') and ApiResource.session.key != os.environ.get('LANCIUM_API_KEY'):
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        url = Job.resource.build_url(Job.base_url, id)
        res = Job.resource.session.delete(url)
        Job.error_handle(res=res, code=202, error_handling=False)

    def destroy(self):
        """Delete a job.

        **DELETE /jobs/<id>**

        ARGS:
            None (None)
        
        RETURNS:
            None: None

        ```python
        from lancium.api.Job import Job

        kwargs = {'name': 'This is a test job', 'image': 'lancium/ubuntu', 'command': 'ls', 'notes': 'this is a note'}
        job = Job.create(**kwargs)

        print(job.name)
        print(job.notes)

        job.destroy()
        print(job.name)
        print(job.notes)

        ###OUTPUT BELOW
        This is a test job
        this is a note
        None
        None

        ```
        """
        Job.delete(self.id, **{'auth': self.__key})

        # Destroy locally
        attrs = self.__dict__
        for key in attrs.keys():
            attrs[key] = None
        self.id = None

    def add_data(self, name, source_type, source, cache=False, jwd_path=None, force=False):
        """Add input data for a job.

        **POST /jobs/<id>/data**

        Args:
        * `name (string)`: filename in the job working directory
        * `source_type (string)`: one of these options ('file', 'data', 'url')
        * `source (string)`: source location of the input data
        * `cache (bool, optional)`: if True, the file is copied to the node during execution as READ ONLY
        * `jwd_path (string, optional)`: path to the job working directory area
        * `force (boolean, optional)`: force add_data if an object exists at specified jwd_path

        Returns:
            JobInput: Job input object
        """
        if not self.__dict__.get('_Job__key') or not self.__key:
            Job.resource.setter(key=os.environ.get('LANCIUM_API_KEY'))
        elif self.__key != ApiResource.session.key:
            Job.resource.setter(key=self.__key)
        Job.input_validation(name = name, source_type=source_type, source=source)
        url = self.resource.build_url(Job.base_url, self.id, 'data' if not jwd_path else 'working_directory/'+str(jwd_path))

        payload = {
            'name': name,
            'source_type': source_type,
            'source': source,
            'cache': cache,
            'auth': self.__key,
            'force': force
        }

        if source_type == 'file':
            payload['size'] = os.path.getsize(source)

        res = self.resource.session.post(url, data=json.dumps(payload))
        Job.error_handle(res=res, code=201, key='input_file')

        data = res.json()['input_file']
        job_input = JobInput(data['id'], self.id, **payload)

        self.input_files.append(job_input)
        return job_input

    def get_jwd(self, folder_path=''):
        '''See what files/directories are at the specified `folder_path`
        
        **HEAD /jobs/<id>/working_directory/<folder_path>**

        ARGS:
        * `folder_path (string)`: path to file/folder in the working directory of a running job
        
        RETURNS:
            Response object: Response Object from the Server

        ```python
        import os
        from lancium.api.Job import Job
        from lancium.errors.common import *
        from time import sleep
        import click

        kwargs = {'name': 'This is a test job', 'image': 'lancium/ubuntu', 'command_line': 'bash bashscript.sh', 'input_files': str(os.path.abspath('bashscript.sh'))}
        job = Job.create(**kwargs)
        file_ = os.path.abspath('bashscript.sh')
        filename = os.path.basename(file_)
        job_input = job.add_data(
            name=filename,
            source_type="file",
            source=file_,
            cache=False)
        progress = click.progressbar(
            length=100,
            show_percent=True,
            label="Uploading input data...",
            fill_char=u'█',
            empty_char=' ',
            bar_template="%(label)s |%(bar)s| %(info)s"
        )

        with progress:
            def progress_callback(
                    current_chunk,
                    total_chunks):
                progress.pos = int(
                    100.0 * current_chunk / total_chunks)
                progress.update(0)

            upload_result = job_input.upload(file_, progress_callback)

        job_input.chunks_received = upload_result["chunks_received"]
        job_input.upload_complete = upload_result["upload_complete"]
        job.submit()

        while job.status != 'running':
            job.refresh()
            sleep(3)

        sleep(30)
        res = job.get_jwd()
        print(res.__dict__)


        ###OUTPUT BELOW
        Uploading input data... |                                    |   0%
        {'_content': b'{"contents":[{"name":"bashscript.sh","is_directory":false,"size":"74","last_modified":"2022-10-05T21:05:46.305+00:00","created":"2022-10-05T21:03:44.000+00:00"},{"name":"stdout.txt","is_directory":false,"size":"362","last_modified":"2022-10-05T21:05:46.352+00:00","created":"2022-10-05T21:05:45.000+00:00"},{"name":"stderr.txt","is_directory":false,"size":"527","last_modified":"2022-10-05T21:05:46.396+00:00","created":"2022-10-05T21:03:48.000+00:00"},{"name":"JOBNAME","is_directory":false,"size":"21","last_modified":"2022-10-05T21:05:46.443+00:00","created":"2022-10-05T21:03:45.000+00:00"},{"name":"rusage-running.json","is_directory":false,"size":"254","last_modified":"2022-10-05T21:05:46.486+00:00","created":"2022-10-05T21:04:46.000+00:00"},{"name":".singularityEnv","is_directory":false,"size":"169","last_modified":"2022-10-05T21:05:46.529+00:00","created":"2022-10-05T21:03:46.000+00:00"},{"name":".bes-info","is_directory":false,"size":"54","last_modified":"2022-10-05T21:05:46.573+00:00","created":"2022-10-05T21:03:43.000+00:00"},{"name":"hosts.txt","is_directory":false,"size":"12","last_modified":"2022-10-05T21:05:46.615+00:00","created":"2022-10-05T21:03:46.000+00:00"},{"name":".genesisII-bes-state","is_directory":true,"size":null,"last_modified":null,"created":null},{"name":"qsub658428181427086480.sh","is_directory":false,"size":"1505","last_modified":"2022-10-05T21:05:46.659+00:00","created":"2022-10-05T21:03:46.000+00:00"}]}', '_content_consumed': True, '_next': None, 'status_code': 200, 'headers': {'Server': 'nginx/1.17.0', 'Date': 'Wed, 05 Oct 2022 21:05:46 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'X-Download-Options': 'noopen', 'X-Permitted-Cross-Domain-Policies': 'none', 'Referrer-Policy': 'strict-origin-when-cross-origin', 'X-Current-API-Version': '1.5.0', 'X-Deprecated-API-Used': 'false', 'X-Object-Type': 'directory', 'Vary': 'Accept,Accept-Encoding', 'ETag': 'W/"598de4181d6688a1e257b3fdc4ec537f"', 'Cache-Control': 'max-age=0, private, must-revalidate', 'X-Request-Id': '69e6ea5f-3d04-47ab-9570-4e1a35be2ad4', 'X-Runtime': '0.735164', 'Content-Encoding': 'gzip'}, 'raw': <urllib3.response.HTTPResponse object at 0x7fed2659a4a0>, 'url': 'https://portal.lancium.com/api/v1/jobs/94521/working_directory/', 'encoding': 'utf-8', 'history': [], 'reason': 'OK', 'cookies': <RequestsCookieJar[]>, 'elapsed': datetime.timedelta(microseconds=786806), 'request': <PreparedRequest [GET]>, 'connection': <requests.adapters.HTTPAdapter object at 0x7fed2697da50>}


        ### BASHSCRIPT.SH

        #!/bin/bash
        i=0
        while [[ $i -lt 600 ]]
        do
        echo "$i"
        sleep 1
        ((i++))
        done
        ```
        '''
        try:
            jwd_path = 'working_directory/' + str(folder_path)
        except:
            raise InvalidInputError(f"Folder path must be a valid string.")

        url = self.resource.build_url(self.base_url,self.id, jwd_path)
        res = self.resource.session.head(url)

        if res.headers.get('X-Object-Type') == 'directory':
            res = self.resource.session.get(url)
        elif res.status_code == 403:
            raise ForbiddenDataError(
                "Requested path '%s' is forbidden." % folder_path)
        elif res.status_code == 503:
            raise UnavailableDataError(
                "Data at '%s' is temporarily unavailable." % folder_path)
        elif res.status_code == 204:
            return res

        try:
            Job.error_handle(res=res, code=200)
        except:
            Job.error_handle(res=res, code=202)

        return res
    

    def download_from_jwd(self, file_path, download_path = None, byte_range_start = None, byte_range_end=None, callback=None):
        '''Download a file from the job working directory.
        
        **GET jobs/<id>/working_directory/<file_path>**

        ARGS:
        * `file_path (string)`: path to file in the job working directory
        * `download_path (string)`: path in local file system to download to
        * `byte_range_start (int, nullable)`: specified start of the byte range user would like to see or download from
        * `byte_range_end (int, nullable)`: specified start of the byte range user would like to see or download to
        * `callback (function)`: function to handle the byte chunks of the file user would like to see. function(status(str), progress (percentage), chunk_of_bytes)
        
        RETURNS:
            String: Range of bytes that have been downloaded. If the status code is 200, will return the "X-File-Size".
        
        ```python
        import os
        from lancium.api.Job import Job
        from time import sleep
        import click

        kwargs = {'name': 'This is a test job', 'image': 'lancium/ubuntu', 'command_line': 'bash bashscript.sh', 'input_files': str(os.path.abspath('bashscript.sh'))}
        job = Job.create(**kwargs)
        file_ = os.path.abspath('bashscript.sh')
        filename = os.path.basename(file_)
        job_input = job.add_data(
            name=filename,
            source_type="file",
            source=file_,
            cache=False)
        progress = click.progressbar(
            length=100,
            show_percent=True,
            label="Uploading input data...",
            fill_char=u'█',
            empty_char=' ',
            bar_template="%(label)s |%(bar)s| %(info)s"
        )

        def progress_callback(
                current_chunk,
                total_chunks):
            progress.pos = int(
                50.0 * current_chunk / total_chunks)
            progress.update(50.0 * current_chunk / total_chunks)

        upload_result = job_input.upload(file_, progress_callback)

        job_input.chunks_received = upload_result["chunks_received"]
        job_input.upload_complete = upload_result["upload_complete"]
        job.submit()

        while job.status != 'running':
            job.refresh()
            sleep(3)

        sleep(30)
        res = job.download_from_jwd(file_path='stdout.txt', download_path=str(os.getcwd()))
        print(os.system('ls stdout.txt'))

        ###OUTPUT BELOW
        Uploading input data... |████████████████████████████████████| 100%
        stdout.txt
        0

        ### Bashscript.sh below

        #!/bin/bash
        i=0
        while [[ $i -lt 600 ]]
        do
        echo "$i"
        sleep 1
        ((i++))
        done

        ```

        '''
        is_dir = False

        if not file_path:
            raise InvalidInputError("Must provide a file path in the Job Working Directory.")
        if download_path:
            if not os.access(download_path, os.W_OK):
                raise InvalidInputError("Specified download path is not writable.")
            filename = os.path.basename(file_path)
            out_path = os.path.join(download_path, filename)
            raw_file = open(out_path, 'wb')
        elif not download_path and not callback:
            raise InvalidInputError("Must provide a download path or callback function.")
        
        try:
            jwd_file_path = 'working_directory/'+str(file_path)
        except:
            raise InvalidInputError(f"File path must be a valid string.")

        url = self.resource.build_url(self.base_url,self.id, jwd_file_path)

        headers = {}
        if (byte_range_start == 0 and byte_range_end == -1) or (byte_range_start == None and byte_range_end == None) :
            headers={}
        elif not byte_range_start and byte_range_end:
            headers['range']=f"bytes=-{byte_range_end}"
        elif not byte_range_end and byte_range_start:
            headers['range'] = f"bytes={byte_range_start}-"
        elif byte_range_start and byte_range_start < 0:
            raise InvalidByteRangeError(
                "Start of byte range cannot be negative.")
        elif byte_range_end and byte_range_end >= 0:
            if byte_range_start > byte_range_end:
                raise InvalidByteRangeError("Start of byte range cannot be "
                                            "after end of byte range.")
            headers['range'] = 'bytes=%d-%d' % (
                byte_range_start, byte_range_end)
        elif (byte_range_start and byte_range_end) and ((byte_range_start == 0 and byte_range_end == -1) or (byte_range_start == None and byte_range_end == None)) :
            headers = {}

        res = ApiResource.session.get(url, headers=headers, stream=True)

        while res.status_code == 202 :
            sleep(5)
            res = ApiResource.session.get(url, headers=headers, stream=True)
        
        if res.status_code == 416:
            raise InvalidByteRangeError(
                "An invalid byte range (%d, %d) was "
                "specified." %
                (byte_range_start, byte_range_end))
        elif res.status_code == 403:
            raise ForbiddenDataError(
                "Requested path '%s' is forbidden." % file_path)
        elif res.status_code == 503:
            raise UnavailableDataError(
                "Data at '%s' is temporarily unavailable." % file_path)
        elif res.status_code == 204:
            return res

        if res.headers.get('X-Object-Type') == 'directory':
            is_dir = True

        if 'range' in headers:
            try:
                Job.error_handle(res, code=206)
            except:
                Job.error_handle(res, code=200)
        else:
            Job.error_handle(res, code=200)

        if is_dir == True:
            raise PathIsDirectoryError("Cannot download directories. '%s' is a directory." % file_path)
        
        current_chunk = 0
        file_size = int(res.headers.get('Content-Length', res.headers.get('X-File-Size',0)))
        total_chunks = ceil(float(file_size) / ApiResource.CHUNK_SIZE)

        if callback:
            callback('downloading', (current_chunk/total_chunks)*100 if total_chunks != 0 else 0, None)

        for chunk in res.iter_content(ApiResource.CHUNK_SIZE):
            if download_path:
                raw_file.write(chunk)
            if callback:
                current_chunk += 1
                callback('downloading', (current_chunk/total_chunks)*100, chunk)

        if download_path:
            raw_file.close()
            
        if res.status_code==200:
            return res.headers.get('X-File-Size')
        return res.headers.get('range') if res.headers.get('range') else res.headers.get('Content-Range')


    def upload_to_jwd(self, source_type, source, jwd_path=None, force=False, callback = None):
        """Add input data to jwd.

        **POST /jobs/<id>/working_directory/<jwd_path>**

        Args:
        * `source_type (string)`: source type of the data to be uploaded ('input_file', 'input_data', 'data_recursive', 'input_url')
        * `source (string)`: file (path in the local file system), input_data (path in the persistent storage area), data_recursive (path in the persistent storage area), url (url)
        * `jwd_path (string)`: path in the job working directory to upload to
        * `force (bool)`: if there is a file already at the jwd_path, upload anyway if set to 'True'
        * `callback (func, optional)`: called after each chunk is successfully uploaded, accepts arguments in the format of (file_size, file_start, total_chunks, current_chunk)

        Returns:
            Response Object: Response Object from the Server

        ```python
        import os
        from lancium.api.Job import Job
        from lancium.errors.common import *
        from time import sleep
        import click

        kwargs = {'name': 'This is a test job', 'image': 'lancium/ubuntu', 'command_line': 'bash bashscript.sh', 'input_files': str(os.path.abspath('bashscript.sh'))}
        job = Job.create(**kwargs)
        file_ = os.path.abspath('bashscript.sh')
        filename = os.path.basename(file_)
        job_input = job.add_data(
            name=filename,
            source_type="file",
            source=file_,
            cache=False)
        progress = click.progressbar(
            length=100,
            show_percent=True,
            label="Uploading input data...",
            fill_char=u'█',
            empty_char=' ',
            bar_template="%(label)s |%(bar)s| %(info)s"
        )

        with progress:
            def progress_callback(
                    current_chunk,
                    total_chunks):
                progress.pos = int(
                    100.0 * current_chunk / total_chunks)
                progress.update(0)

            upload_result = job_input.upload(file_, progress_callback)

        job_input.chunks_received = upload_result["chunks_received"]
        job_input.upload_complete = upload_result["upload_complete"]
        job.submit()

        while job.status != 'running':
            job.refresh()
            sleep(3)

        sleep(30)
        def callback(current_chunk, total_chunks):
            pass
        res = job.upload_to_jwd(source_type='file', source=str(os.path.abspath('asd.py')), jwd_path='asd.py', force=True, callback=callback)
        print(os.system('ls asd.py'))


        ###OUTPUT BELOW
        Uploading input data... |                                    |   0%
        asd.py
        0
        ```
        """
        if source_type not in {'file', 'data', 'url', 'data_recursive'}:
            raise InvalidInputTypeError(
                "Invalid Job input source type provided. "
                "Can be one of 'file', 'data', 'data_recursive' or 'url'.")
        if not source:
            raise InvalidInputError("Invalid Job input source provided.")
        
        url = self.resource.build_url(self.base_url,self.id, 'working_directory/')
        payload = {
            'source_type': source_type,
            'source': source,
            'force': force,
            'path': jwd_path
        }

        if source_type == 'file':
            payload['size'] = os.path.getsize(source)

        res = self.resource.session.post(url, data=json.dumps(payload))
        Job.error_handle(res=res, code = 202)

        if source_type == 'file' and not os.path.isfile(source):
                raise InvalidInputError("Invalid Job Working Directory Input file path provided.")
        if source_type == 'file':
            url = self.resource.build_url(self.base_url,self.id, 'working_directory/'+jwd_path)
            res = self.resource.handle_upload(url, source, callback)
            self.resource._verify_response(res, 201)
            if not res.json()['upload_complete']:
                raise InternalError("Upload failed.")
        try:
            data = res.json()
        except:
            data = res
        return data


    def __init__(self, id=None, **kwargs):
        """This class interacts with Lancium Jobs. It allows you to create, update, run, terminate, suspend, interact with the working directory of a running job, and delete jobs.

        Args:
        * `__key` (string): auth key
        * `id` (int, should not pass): Job ID
        * `name` (string): Job name
        * `notes` (string): Job description
        * `status` (string): Job status
        * `qos` (string): Job quality of service (high, low, medium)
        * `command_line` (string): command line argument for Job
        * `image` (string): Image to use for Job
        * `resources` (string): Job resources (CPU's, GPU's, Scratch, etc.)
        * `max_run_time` (int): Job's max run time in seconds (up to a month)
        * `expected_run_time` (int): expected run time of Job 
        * `input_files` (JobInput): input files for Job
        * `output_files` (File): output files available after Job completion
        * `callback_url` (string): url to send Job updates to
        * `mpi` (boolean): boolean flag for whether the Job runs MPI
        * `mpi_version` (string): which flavor of MPI to use
        * `tasks` (int): how many MPI tasks total
        * `tasks_per_node` (int): how many MPI tasks per node
        """
        if kwargs.get('transaction'):
            Job.resource.set_transaction(transaction=kwargs.get('transaction'))
        self.__key = self.__dict__.get('_Job__key')
        if kwargs.get('auth') and not self.__key:
            self.__key = kwargs.get('auth')
            self.resource.setter(key=kwargs.get('auth'))
        if not self.resource.session:
            raise MissingCredentialsError("Missing credentials.")

        self.id = id
        self.name = kwargs.get('name')
        self.notes = kwargs.get('notes')
        self.account = kwargs.get('account')
        self.status = kwargs.get('status')
        self.qos = kwargs.get('qos')
        self.command_line = kwargs.get('command_line')
        self.image = kwargs.get('image')
        self.resources = kwargs.get('resources', {})
        self.max_run_time = kwargs.get('max_run_time')
        self.expected_run_time = kwargs.get('expected_run_time')
        self.input_files = kwargs.get('input_files', [])
        self.output_files = kwargs.get('output_files', [])
        self.callback_url = kwargs.get('callback_url')
        self.mpi = kwargs.get('mpi')
        self.mpi_version = kwargs.get('mpi_version')
        self.tasks = kwargs.get('tasks')
        self.tasks_per_node = kwargs.get('tasks_per_node')
