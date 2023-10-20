from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from answer_rocket.auth import AuthHelper

from answer_rocket.graphql.schema import Query, Mutation


class GraphQlClient:

    def __init__(self, auth_helper: AuthHelper):
        self._endpoint = HTTPEndpoint(
            url=auth_helper.url + "/api/sdk/graphql",
            base_headers=auth_helper.headers())
        
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
    