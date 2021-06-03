from django.conf import settings
from django.shortcuts import render
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractYear
from django.db.models import Sum, Count
from django.views.generic import ListView, DetailView, FormView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from django.utils import timezone
import json, pytz

from . import models, forms


class EntriesView(LoginRequiredMixin, View):
    login_url = 'account:readme_page'
    template_name = 'report/entries.html'
    context = {}

    def get(self, *args, **kwargs):
        qs = models.Entries.objects.filter(user=self.request.user)
        entries = qs.order_by('-date')
        date_min = self.request.GET.get('date_min')
        date_max = self.request.GET.get('date_max')
        date_ordering = self.request.GET.get('orderingSelect')

        if self.is_valid_queryparam(date_ordering):
            entries = qs.order_by(date_ordering)

        if self.is_valid_queryparam(date_min):
            entries = entries.filter(date__gte=date_min)

        if self.is_valid_queryparam(date_max):
            entries = entries.filter(date__lt=date_max)
        
        self.context['data'] = entries
        return render(self.request, self.template_name, self.context)
    
    def is_valid_queryparam(self, param):
        return param != '' and param is not None


class EntriesStatsView(LoginRequiredMixin, ListView):
    login_url = 'account:readme_page'
    context_object_name = 'weeks'
    template_name = 'report/stats.html'

    def get_queryset(self):
        queryset = models.EntriesStatistics.objects.filter(user=self.request.user)[:53]
        return queryset


class EntriesDetailView(DetailView):
    model = models.Entries
    context_object_name = 'object'
    template_name = "report/entries-detail.html"


class EntriesCreateView(LoginRequiredMixin, CreateView):
    login_url = 'account:readme_page'

    model = models.Entries
    form_class = forms.ReportCreateForm
    template_name = 'report/entrie-form.html'
    success_url = reverse_lazy('report:entries')

    def form_valid(self, form):
        form_date = form.cleaned_data['date']
        distance = form.cleaned_data['distance']
        duration = form.cleaned_data['duration']
        week_num = form_date.isocalendar()[1]
        qs = models.EntriesStatistics.objects.filter(
            user=self.request.user, 
            week_number=week_num
        )

        # add to Entries form creation
        form.instance.user = self.request.user
        form.instance.week_number = week_num

        if qs.exists():
            qs = qs[0]
            qs.amount_of_entries = qs.amount_of_entries+1
            qs.total_distance=qs.total_distance+float(distance)
            qs.total_duration=qs.total_duration+duration
            qs.save()
        else:
            stats = models.EntriesStatistics.objects.create(
                week_number=week_num,
                amount_of_entries=1,
                total_distance=distance,
                total_duration=duration,
                user=self.request.user
            )
        return super().form_valid(form)
    

class EntriesDeleteView(DeleteView):
    model = models.Entries
    template_name = 'report/confirm-delete.html'
    success_url = reverse_lazy('report:entries')

    def get_object(self, queryset=None):
        obj = super(EntriesDeleteView, self).get_object()
        return obj

    def post(self, request, *args, **kwargs):
        obj = self.get_object()

        entr_stat = models.EntriesStatistics.objects.get(week_number=obj.week_number)
        if entr_stat.amount_of_entries == 1:
            entr_stat.delete()
        else:
            entr_stat.amount_of_entries = entr_stat.amount_of_entries - 1
            entr_stat.total_distance = entr_stat.total_distance - float(obj.distance)
            entr_stat.total_duration = entr_stat.total_duration - obj.duration
            entr_stat.save()
        return self.delete(request, *args, **kwargs)

    