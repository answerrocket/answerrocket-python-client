from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

from answer_rocket.auth import AuthHelper

from answer_rocket.graphql.schema import Query


class GraphQlClient:

    def __init__(self, auth_helper: AuthHelper):
        self._endpoint = HTTPEndpoint(
            url=auth_helper.url + "/api/sdk/graphql",
            base_headers=auth_helper.headers())
        
    def submit(self, operation, variables=None):
        raw_response = self._endpoint(operation, variables)
        return operation + raw_response
    
    def query(self, variables: dict | None = None):
        if variables:
            return Operation(Query, variables=variables)
        return Operation(Query)
    