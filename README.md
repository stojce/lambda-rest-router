# AWS Lambda REST Router

Example usage:

```python
from lambda_rest_router import LambdaRouter


routes = {
    "agencies": {
        "GET": "api.services.agency/AgencyService:list_agencies",
        "POST": "api.services.agency/AgencyService:create_agency",
    },
    "agencies/<_id>": {
        "GET": "api.services.agency/AgencyService:get_agency",
        "POST": "api.services.agency/AgencyService:update_agency",
    },
    "users/agency/<agency_id>": {
        "GET": "api.services.user/UserService:list_agency_users",
        "POST": "api.services.user/UserService:create_user",
    },
    "users": {
        "GET": "api.services.user/UserService:list_users",
        "POST": "api.services.user/UserService:create_user",
    },
    "users/<_id>": {
        "GET": "api.services.user/UserService:get_user",
        "POST": "api.services.user/UserService:update_user",
    },
    "datafiles": {
        "POST": "api.services.datafile/DataFileService:create_file_upload_url",
    },
}
router = LambdaRouter(routes)

def handler(event, context):

    # ctx is a context object that will be passed to the route
    # e.g.
    # ctx = {
    #     "user": {
    #         "uid": claims["sub"],
    #         "role": role,
    #     }
    # }
    ctx = {}
    return router.call_route(event, ctx)


```
