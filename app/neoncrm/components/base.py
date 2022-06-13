"""NeonCRM API V2 Python Client"""

from app.neoncrm import util


class BaseComponent(util.API):
    """A base component"""

    def __init__(self, base_uri=None, auth=None, timeout=15, **kwargs):
        """Setup a base component

        :param base_uri: The base URI to the API
        :param access_token: The JSON Web token
        :param timeout: The timeout to use for requests
        :param \*\*kwargs: Any other attributes. These will be added as
                           attributes to the ApiClient object.
        """
        super(BaseComponent, self).__init__(
            base_uri=base_uri, timeout=timeout, 
            auth=auth, **kwargs)

        # Create an HTTP Authorization Header
        self.headers = {
            "Authorization" : "Basic basic_auth_token",
            "NEON-API-VERSION" : "2.1"
        }

    def get_request(
            self, endpoint, params=None, headers=None):
        """Helper function for GET requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param headers: request headers
        :return: The :class:``requests.Response`` object for this request
        """
        headers = headers or {}
        headers.update(self.headers)
        return super(BaseComponent, self).get_request(
            endpoint, params=params, headers=headers)

    def post_request(
            self, endpoint, params=None, data=None, json=None, headers=None):
        """Helper function for POST requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data (either as a dict or dumped JSON string) to
                     include with the POST
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        headers = headers or {}
        headers.update(self.headers)
        return super(BaseComponent, self).post_request(
            endpoint, params=params, data=data, json=json, headers=headers)

    def put_request(
            self, endpoint, params=None, json=None, headers=None):
        """Helper function for PUT requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data (either as a dict or dumped JSON string) to
                     include with the PUT
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        headers = headers or {}
        headers.update(self.headers)
        return super(BaseComponent, self).put_request(
            endpoint, params=params, json=json, headers=headers)

    def patch_request(
            self, endpoint, params=None, json=None, headers=None):
        """Helper function for PATCH requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data (either as a dict or dumped JSON string) to
                     include with the PATCH
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        headers = headers or {}
        headers.update(self.headers)
        return super(BaseComponent, self).patch_request(
            endpoint, params=params, json=json, headers=headers
        )

    def delete_request(
            self, endpoint, params=None, json=None, headers=None, cookies=None):
        """Helper function for DELETE requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data (either as a dict or dumped JSON string) to
                     include with the DELETE
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        headers = headers or {}
        headers.update(self.headers)
        return super(BaseComponent, self).delete_request(
            endpoint, params=params, json=json, headers=headers,
            cookies=cookies)
