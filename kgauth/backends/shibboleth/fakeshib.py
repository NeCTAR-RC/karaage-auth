import random
import string

from django import forms
from django.views.generic.edit import FormView

from karaage.people.models import Person


shib_headers = [
    'CN', 'DISPLAYNAME', 'GIVENNAME', 'SN', 'UID', 'EPPN',
    'L', 'EMPLOYEETYPE', 'DESCRIPTION', 'O', 'AFFILIATION',
    'UNSCOPED-AFFILIATION', 'ASSURANCE', 'SHIB_IDENTITY_PROVIDER',
    'SHARED_TOKEN', 'HOMEORGANIZATION', 'HOMEORGANIZATIONTYPE',
    'TELEPHONENUMBER']
shib_headers += ['SHIB_SESSION_ID']


class PersonModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s (%s)" % (obj.full_name, obj.email)


class FakeShibForm(forms.Form):
    user = PersonModelChoiceField(
        label='Existing user',
        queryset=Person.objects.filter(saml_id__isnull=False),
        required=False)
    username = forms.CharField(label='New username',
                               max_length=255,
                               required=False)


class FakeShibView(FormView):
    template_name = 'shibboleth/fakeshib.html'
    form_class = FakeShibForm
    success_url = '/shibboleth/'

    def get_success_url(self):
        next_path = self.kwargs.get('next_path')
        return '%s%s' % (self.success_url, next_path)

    def get_context_data(self, **kwargs):
        context = super(FakeShibView, self).get_context_data(**kwargs)
        context['next_path'] = self.kwargs.get('next_path')
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        user = form.cleaned_data['user']

        session = self.request.session
        session["fakeshib"] = {}
        if user:
            persistent_id = user.saml_id
            email = user.email
        else:
            persistent_id = username
            email = username

        session["fakeshib"]["HTTP_PERSISTENT_ID"] = persistent_id
        session["fakeshib"]["HTTP_MAIL"] = email

        # encode shib headers
        for header in shib_headers:
            session["fakeshib"]['HTTP_' + header] = ''.join(
                random.choice(string.letters + string.digits)
                for i in xrange(20))
        session.modified = True
        return super(FakeShibView, self).form_valid(form)
