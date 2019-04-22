
from .blueprint import web


@web.after_request
def see_cache(b):
    pass


@web.after_app_request
def after_request(response):
    pass
