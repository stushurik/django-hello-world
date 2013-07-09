import json
from django.contrib.auth.models import User
from django_hello_world.hello.models import WebRequest


def dumps(value):
    return json.dumps(value, default=lambda o: None)


class WebRequestMiddleware(object):
    def process_request(self, request):
        user = request.user if isinstance(request.user, User) else None
        meta = request.META.copy()
        meta.pop('QUERY_STRING', None)
        meta.pop('HTTP_COOKIE', None)
        remote_addr_fwd = None

        if 'HTTP_X_FORWARDED_FOR' in meta:
            remote_addr_fwd = \
                meta['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
            if remote_addr_fwd == meta['HTTP_X_FORWARDED_FOR']:
                meta.pop('HTTP_X_FORWARDED_FOR')

        WebRequest(
            host=request.get_host(),
            path=request.path,
            method=request.method,
            uri=request.build_absolute_uri(),
            user_agent=meta.pop('HTTP_USER_AGENT', None),
            remote_addr=meta.pop('REMOTE_ADDR', None),
            remote_addr_fwd=remote_addr_fwd,
            meta=None if not meta else dumps(meta),
            cookies=None if not request.COOKIES else dumps(request.COOKIES),
            get=None if not request.GET else dumps(request.GET),
            post=None if not request.POST else dumps(request.POST),
            raw_post=request.read(),
            is_secure=request.is_secure(),
            is_ajax=request.is_ajax(),
            user=user
        ).save()
