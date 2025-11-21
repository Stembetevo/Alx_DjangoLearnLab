from django.utils.deprecation import MiddlewareMixin


class ContentSecurityPolicyMiddleware(MiddlewareMixin):
    """Simple middleware that adds a conservative Content-Security-Policy header.

    Adjust the policy to match your asset hosts. This header reduces the
    risk of XSS by restricting allowed sources for scripts, styles, images, etc.
    """

    def process_response(self, request, response):
        # Minimal CSP: allow content from same origin, images from data:, styles/scripts only self
        policy = "default-src 'self'; img-src 'self' data:; script-src 'self'; style-src 'self' 'unsafe-inline'"
        # If a header is already present do not overwrite it
        if 'Content-Security-Policy' not in response:
            response['Content-Security-Policy'] = policy
        return response
