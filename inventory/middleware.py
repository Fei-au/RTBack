# import logging
# import json
# from django.utils.deprecation import MiddlewareMixin
#
# logger = logging.getLogger('django')
#
#
#
# # class RequestResponseLogMiddleware(MiddlewareMixin):
# #     def process_request(self, request):
# #         # Log the 'item' attribute if it's a part of the form data
# #         if request.method in ['POST', 'PUT', 'PATCH']:
# #             item = request.POST.get('item', None)
# #             if item is not None:
# #                 logger.info(f"Request: {request.method} {request.get_full_path()}, Item: {item}")
# #             # Handle files differently to avoid decoding issues
# #             if 'image' in request.FILES:
# #                 logger.info(f"Request: {request.method} {request.get_full_path()}, contains file uploads")
# #         else:
# #             logger.info(f"Request: {request.method} {request.get_full_path()}")
# #
# #     def process_response(self, request, response):
# #         # Response processing, assuming JSON or text as before
# #         content_type = response['Content-Type']
# #         if 'application/json' in content_type or 'text' in content_type:
# #             try:
# #                 response_body = response.content.decode('utf-8')
# #                 logger.info(f"Response: {response.status_code} {request.get_full_path()}, Body: {response_body}")
# #             except UnicodeDecodeError:
# #                 logger.info(f"Response: {response.status_code} {request.get_full_path()} contains binary data")
# #         else:
# #             logger.info(f"Response: {response.status_code} {request.get_full_path()} - Non-text content type: {content_type}")
# #         return response