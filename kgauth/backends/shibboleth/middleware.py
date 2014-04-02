import re

from django.shortcuts import redirect


class FakeShibMiddleware(object):
    def process_request(self, request):
        fakeshib = request.session.get('fakeshib')
        if fakeshib:
            request.environ.update(fakeshib)
            del request.session['fakeshib']

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            match = re.match(r'/shibboleth/(?P<next_path>.*)$', request.path)
            if match:
                # Redirect to the fakeshib view, which allows the user to
                # select a Person to log in as, and sets session['fakeshib'].
                return redirect('kgauth_fakeshib', **match.groupdict())
