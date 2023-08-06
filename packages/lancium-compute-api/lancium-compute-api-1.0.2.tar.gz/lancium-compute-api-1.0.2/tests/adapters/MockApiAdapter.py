from urllib import request
from requests.adapters import BaseAdapter
from requests import Response
from urllib3 import HTTPResponse
import random
import json
import six
import jwt
import time
import datetime
import os


class MockApiAdapter(BaseAdapter):

    def __init__(self, template_path="templates"):
        super().__init__()
        folder_path = os.path.dirname(os.path.abspath(__file__))
        self.BASE_PATH = os.path.join(folder_path, template_path)

    def build_json(self, method, path_url):
        """Builds response given request URL.

        Args:
            method (string): HTTP verb
            path_url (string): url path

        Returns:
            HTTPResponse: response
        """
        file_path = '{}.json'.format(os.path.join(
            self.BASE_PATH, path_url[1:], method))

        body = None
        is_json = False

        if os.path.exists(file_path):  # JSON file
            try:
                with open(file_path) as json_file:
                    data = json.load(json_file)

                # Convert JSON data to a IOReader
                text = json.dumps(data)
                content = text.encode('utf-8')
                body = _IOReader(content)
                is_json = True
            except BaseException:
                pass
        else:
            file_path = os.path.join(self.BASE_PATH, path_url[1:])
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as raw_file:
                        data = raw_file.read()

                    body = _IOReader(data)
                except BaseException:
                    pass

        if is_json:
            headers = {'content-type': 'application/json'}
            if 'file' not in path_url[1:]:
                headers['X-Object-Type'] = 'directory'
        else:
            headers = {'content-type': 'application/octet-stream'}
            if 'file' not in path_url[1:]:
                headers['X-Object-Type'] = 'directory'
        # Create mock HTTPResponse
        raw = HTTPResponse(status=200,
                           reason=six.moves.http_client.responses.get(
                               200),
                           headers=headers,
                           body=body or _IOReader(six.b('')),
                           decode_content=False,
                           preload_content=False)
        return raw

    def build_response(self, req, resp):
        """Builds a response object.

        Params:
            req (request)
            resp (HTTPResponse)

        Returns:
            response
        """
        response = Response()

        # Fallback to None if there's no status_code, for whatever reason.
        response.status_code = getattr(resp, 'status', None)
        response.raw = resp
        response.reason = response.raw.reason
        response.headers.update(getattr(resp, 'headers', {}))

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')
        else:
            response.url = req.url

        # Give the Response some context.
        response.request = req
        response.connection = self

        return response

    def send(self, request, stream=False, timeout=None, verify=True,
             cert=None, proxies=None):
        """Returns a templated Response object.

        Args:
            request (request): request object provided by the request session.

        Returns:
            response
        """
        body = self.build_json(request.method, request.path_url)
        response = self.build_response(request, body)
        self._custom_url_handler(request, response)
        return response

    def close(self):
        """Empty function needed to implement BaseAdapter.
        """
        pass

    def _custom_url_handler(self, req, resp):
        """Handles endpoints that don't return raw JSON and sets appropriate
        HTTP status codes.

        Args:
            request (request): request object provided by the request session.
            resp (response): empty response
        """
        method = req.method
        path_url = req.path_url

        if path_url == '/access_tokens':
            resp.status_code = 201
            resp.headers['Authorization'] = 'Bearer {}'.format(jwt.encode({
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, 'secret'))
            return

        url_parts = os.path.normpath(path_url).split(os.path.sep)

        request_path = os.path.join(self.BASE_PATH, path_url[1:])
        file_path = '{}.json'.format(os.path.join(
            self.BASE_PATH, path_url[1:], method))

        if not os.path.exists(file_path) and not os.path.exists(request_path):
            if '?recursive=true' in file_path or '?recursive=true' in request_path:
                tmp_file_path = file_path.replace('?recursive=true', '')
                tmp_request_path = request_path.replace('?recursive=true','')
                if not os.path.exists(tmp_file_path) and not os.path.exists(tmp_request_path):
                    resp.status_code = 404
                    return
            else:
                resp.status_code = 404
                return
            
            

        if method == 'GET':
            resp.headers.update(
                {'Content-Length': os.path.getsize(request_path)})
            if 'working_directory' in path_url[1:] and 'file' not in path_url[1:]:
                file_path = os.path.join(
                    self.BASE_PATH, f"{path_url[1:]}{method}.json" if not method else f"{path_url[1:]}/{method}.json")
                if '//' in file_path:
                    file_path = file_path.replace('//','/')
                if not os.path.exists(file_path):
                    resp.status_code = 404
                if os.path.isdir(file_path):
                    resp.status_code = 422
                if os.path.exists(file_path):
                    with open(file_path) as json_file:
                        data = json.load(json_file)
                    resp.headers.update(data)

        if method == 'HEAD':
            if 'working_directory' in path_url[1:]:
                resp.status_code=202
            else:
                resp.status_code = 204

            if 'working_directory' not in path_url[1:]:
                file_path = os.path.join(
                    self.BASE_PATH, '{}_{}.json'.format(path_url[1:], method))
            else:
                file_path = os.path.join(
                    self.BASE_PATH, '{}{}.json'.format(path_url[1:], method))
            if not os.path.exists(
                    file_path) and not os.path.exists(request_path):
                resp.status_code = 404
                return

            if os.path.isdir(request_path if 'working_directory' not in path_url[1:] else file_path):
                resp.status_code = 422
                return

            if os.path.exists(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                resp.headers.update(data)
            else:
                resp.status_code = 404
        if method == 'POST':
            if url_parts[1] == 'data':
                resp.status_code = 202
            else:
                if 'working_directory' in url_parts[1:]:
                    resp.status_code = 202
                else:
                    resp.status_code = 201

        if method == 'PUT' and url_parts[1] == 'jobs':
            if os.path.exists(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)['job']
                if data['status'] != 'created':
                    resp.status_code = 409
                    return
            else:
                resp.status_code = 404
                return

        if method == 'PATCH':
            resp.status_code = 202
            if os.path.exists(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                resp.headers.update(data)
            else:
                resp.status_code = 404
                return

            state_path = os.path.join(
                self.BASE_PATH, path_url[1:], '_state.json')
            if os.path.exists(state_path):
                with open(state_path) as json_file:
                    data = json.load(json_file)
                if 'size' in data:
                    size = data['size']
                    if 'Content-Length' in req.headers:
                        current_offset = int(
                            req.headers['Upload-Offset']) + int(req.headers['Content-Length'])
                        if current_offset >= size:
                            resp.status_code = 201
                    else:
                        resp.status_code = 411
                        return
                else:
                    resp.status_code = 500
                    return
            else:
                resp.status_code = 500
                return

            wait_time = random.random()
            time.sleep(wait_time if wait_time < 0.5 else 0.5)

        if method == 'DELETE':
            resp.status_code = 202
            if 'data' in url_parts and 'job' not in ' '.join(url_parts) and 'file' not in ' '.join(url_parts) and 'recursive=true' not in ' '.join(url_parts):
                resp.status_code=409

        if url_parts[-1] == 'submit':
            if 'errors' in resp.json():
                resp.status_code = 400
            else:
                resp.status_code = 202
            return

        if url_parts[-1] in {'suspend', 'terminate', 'rebuild'}:
            resp.status_code = 202

class _IOReader(six.BytesIO):
    """A reader that makes a BytesIO look like a HTTPResponse.

    A HTTPResponse will return an empty string when you read from it after
    the socket has been closed. A BytesIO will raise a ValueError. For
    compatibility we want to do the same thing a HTTPResponse does.
    """

    def read(self, *args, **kwargs):
        if self.closed:
            return six.b('')

        result = six.BytesIO.read(self, *args, **kwargs)
        if result == six.b(''):
            self.close()

        return result
