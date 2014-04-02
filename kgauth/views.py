from django.views.generic.base import TemplateView


class LoginSelectView(TemplateView):
    template_name = "kgauth/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginSelectView, self).get_context_data(**kwargs)
        context['next_path'] = self.request.GET.get('next')
        return context
