from pydevlake.api import API, APIException, Paginator, Request, Response, request_hook, response_hook

class CommerceCloudAPI(API):
    base_url = "https://portalapi.commerce.ondemand.com/v2/subscriptions/"

    @request_hook
    def authenticate(self, request: Request):
        request.headers['Authorization'] = 'Basic ' + self.connection.token

    def get_environments(self):
        return self.get(self.connection.subscription_code, 'environments')

    def get_deployment(self, deployment_code:str):
        return self.get(self.connection.subscription_code, 'deployments', deployment_code)

    def get_deployments(self):
        return self.get(self.connection.subscription_code, 'deployments')

    def get_build(self, build_code: str):
        return self.get(self.connection.subscription_code, 'builds', build_code)
    
    def get_builds(self):
        return self.get(self.connection.subscription_code, 'builds')

