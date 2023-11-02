import json
from .utils import *
from werkzeug import Request, Response
from nameko.web.handlers import HttpRequestHandler
from apollo_shared.exception import ApolloException


class HttpEntrypoint(HttpRequestHandler):

    def handle_request(self, request: Request):
        request.context = start_context(request)
        return super().handle_request(request)

    def response_from_exception(self, exc) -> Response:
        status_code = 500

        if isinstance(exc, ApolloException):
            status_code = exc.status_code
            error_message = str(exc)
        else:
            error_message = "Error - Contact Erfan Sahebi - " + str(exc)

        response_data = {
            'error': error_message,
        }

        return Response(
            response=json.dumps(response_data),
            status=status_code,
            mimetype='application/json'
        )


http = HttpEntrypoint.decorator
