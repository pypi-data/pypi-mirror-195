from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.http import urlencode
from django.views import generic

from mpi_cbs.mediforms.forms import TokenForm
from mpi_cbs.mediforms.models import Token


class Index(LoginRequiredMixin, generic.FormView):
    form_class = TokenForm
    template_name = 'mediforms/index.html'

    def get_context_data(self):
        context_data = super().get_context_data()
        context_data['method'] = self.request.GET.get('method', '')
        context_data['token'] = self.request.GET.get('token', '')
        return context_data

    def post(self, request, *args, **kwargs):
        token, _created = Token.objects.get_or_create(
            method_id=request.POST.get('method'),
            pseudonym=request.POST.get('pseudonym'),
            defaults=dict(created_by=self.request.user),
        )
        params = urlencode(dict(
            token=token.id,
            method=token.method,
        ))
        return HttpResponseRedirect('{}?{}'.format(reverse('index'), params))


class FormView(generic.TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(Token, pk=kwargs.get('token'))
        self.method = self.token.method
        return super().dispatch(request, *args, **kwargs)

    def get_template_name(self):
        return [f'consents/pages/form_{self.method.id}.html']
