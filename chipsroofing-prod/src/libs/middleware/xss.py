class XSSProtectionMiddleware(object):
    @staticmethod
    def process_response(request, response):
        # Don't set it if it's already in the response
        if response.get('X-XSS-Protection', None) is not None:
            return response

        response['X-XSS-Protection'] = '1; mode=block'
        return response
