# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

class CalculateView(TemplateView):
    template_name = 'calculate.html'

    def post(self, request, *args, **kwargs):
        context = dict(f='123')
        return super(CalculateView, self).render_to_response(context)

calculate = CalculateView.as_view()
