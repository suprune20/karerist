# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.http import HttpResponse
from django.views import View

class MyView(View):
    template_name = 'calculate.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = dict(f='123')
        return render(request, self.template_name, context)

calculate = MyView.as_view()
