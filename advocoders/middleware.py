from django.core.urlresolvers import resolve

class ViewNameMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path).url_name
        request.current_view = url_name
