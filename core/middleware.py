import time

class RequestExecutionTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        print(f"{request.method} {request.path} took {end_time - start_time:.4f} seconds")

        return response