from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from answer_rocket.auth import AuthHelper, init_auth_helper
from answer_rocket.client_config import ClientConfig

from answer_rocket.graphql.schema import Query, Mutation


class GraphQlClient:

    def __init__(self, config: ClientConfig):
        self._auth_helper = init_auth_helper(config)
        self._endpoint = HTTPEndpoint(
            url=self._auth_helper.config.url + "/api/sdk/graphql",
            base_headers=self._auth_helper.headers())
        
    def submit(self, operation, variables=None):
        raw_response = self._endpoint(operation, variables)

        if 'errors' in raw_response:
            raise Exception(raw_response['errors'][0]['message'])
        if 'errorMessage' in raw_response:
            raise Exception(raw_response['errorMessage'])

        return operation + raw_response
    
    def query(self, variables: dict | None = None):
        if variables:
            return Operation(Query, variables=variables)
        return Operation(Query)

    def mutation(self, variables: dict | None = None):
        if variables:
            return Operation(Mutation, variables=variables)
        return Operation(Mutation)
    