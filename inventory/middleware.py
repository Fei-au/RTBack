import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django')


class RequestResponseLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_body = request.body
        if request_body:
            try:
                request_body = json.loads(request_body)
            except json.JSONDecodeError:
                request_body = request_body.decode('utf-8')
        logger.info(f"Request: {request.method} {request.get_full_path()}, Body: {request_body}")

    def process_response(self, request, response):
        response_body = response.content
        if response_body:
            try:
                response_body = json.loads(response_body)
            except json.JSONDecodeError:
                response_body = response_body.decode('utf-8')
        logger.info(f"Response: {response.status_code} {request.get_full_path()}, Body: {response_body}")
        return response