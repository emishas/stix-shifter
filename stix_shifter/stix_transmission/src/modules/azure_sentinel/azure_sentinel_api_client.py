from ..utils.RestApiClient import RestApiClient


class APIClient:
    """API Client to handle all calls."""
    PING_TIMEOUT_IN_SECONDS = 10
    
    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        headers = dict()
        url_modifier_function = None
        default_api_version = 'v1.0'
        auth = configuration.get('auth')
        self.endpoint = '{api_version}/security/alerts'.format(api_version=default_api_version)
        self.host = connection.get('host')

        if auth:
            if 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port', None),
                                    connection.get('cert', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    mutual_auth=connection.get('use_securegateway', False),
                                    sni=connection.get('sni', None)
                                    )

    def ping_box(self):
        """Ping the endpoint."""
        params = dict()
        params['$top'] = 1
        return self.client.call_api(self.endpoint, 'GET', urldata=params, timeout=self.PING_TIMEOUT_IN_SECONDS)

    def run_search(self, query_expression, length):
        """get the response from azure_sentinel endpoints
        :param query_expression: str, search_id
        :param length: int,length value
        :return: response, json object"""
        headers = dict()
        headers['Accept'] = 'application/json'
        params = dict()
        params['$filter'] = query_expression
        params['$top'] = length
        return self.client.call_api(self.endpoint, 'GET', headers, urldata=params)

    def next_page_run_search(self, next_page_url):
        """get the response from azure_sentinel endpoints
        :param next_page_url: str, search_id
        :return: response, json object"""
        headers = dict()
        headers['Accept'] = 'application/json'
        url = next_page_url.split('?', maxsplit=1)[1]
        endpoint = self.endpoint + '?' + url
        return self.client.call_api(endpoint, 'GET', headers)
