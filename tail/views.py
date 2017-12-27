from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class TailLogView(LoginRequiredMixin, TemplateView):
    template_name = 'tail/tail.html'
 
    def get(self, request, *args, **kwargs):
        return super(TailLogView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        log_list = getattr(settings, 'LOGTAIL_FILES', [])
        log_list = [log.rsplit('/', 1)[-1].split('.')[0] for log in log_list]

        lines_displayed = getattr(settings, 'LOGTAIL_LINES_DISPLAYED', 300)
        ctx = super(TailLogView, self).get_context_data(**kwargs)
        ctx['lines_displayed'] = lines_displayed
        ctx['log_list'] = log_list

        return ctx
