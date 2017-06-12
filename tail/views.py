from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TailLogView(LoginRequiredMixin, TemplateView):
    template_name = 'tail/tail.html'
 
    def get(self, request, *args, **kwargs):
        #print(dir(request.session))
        return super(TailLogView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(TailLogView, self).get_context_data(**kwargs)
        ctx['logtail_file'] = getattr(settings, 'LOGTAIL_FILE', '')

        return ctx
