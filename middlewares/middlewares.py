class CORSMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = 'client-timezone, authorization, content-type'
        response["Access-Control-Allow-Credentials"] = 'true'
        response["Access-Control-Allow-Methods"] = 'GET, PUT, POST, PATCH, DELETE, HEAD'

        return response
