from collections import OrderedDict
import datetime

from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from jet.dashboard.modules import DashboardModule

from people import models as people_models


class TagPopularityChart(DashboardModule):
    """
    Chart.js widget that shows tag popularity
    """

    title = _('Tag popularity chart')
    template = 'dashboard/modules/tag_popularity_chart.html'
    style = 'overflow-x: auto;'
    max_chart_items = 4

    class Media:
        js = (
            'people/tag_popularity_chart.js',
        )

    def init_with_context(self, context):
        result = people_models.PersonTag.objects.values('tag__value').annotate(
            tag_count=Count('tag__value')).order_by('-tag_count')

        count = 0
        for data in result:
            self.children.append((data['tag__value'], data['tag_count']))
            if count >= self.max_chart_items:
                break
            count = count + 1


class TagsOverTimeChart(DashboardModule):
    """
    Chart.js widget that shows tags by hour
    """

    title = _('Tags by hour')
    template = 'dashboard/modules/tags_over_time_chart.html'
    style = 'overflow-x: auto;'
    hours = 24

    class Media:
        js = (
            'people/tags_over_time_chart.js',
        )

    def init_with_context(self, context):
        start_time = timezone.now() - datetime.timedelta(hours=self.hours)
        result = people_models.PersonTag.objects.filter(created_at__gt=start_time).extra(
            select={'hour': "date_part(\'hour\', \"created_at\")"}).values('hour').order_by('hour')

        results_dict = OrderedDict()
        for hour in range(1, self.hours + 1):
            current = start_time + datetime.timedelta(hours=hour)
            results_dict[int(current.hour)] = 0

        for data in result:
            results_dict[int(data['hour'])] += 1

        for key, value in results_dict.items():
            self.children.append((key, value))


class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(TagPopularityChart)
        self.available_children.append(TagsOverTimeChart)

        self.children.append(modules.LinkList(
            _('Resources'),
            children=[
                {
                    'title': _('Source code'),
                    'url': 'https://github.com/jessamynsmith/django_jet_example',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ],
            column=0,
            order=1
        ))

        self.children.append(TagsOverTimeChart(
            _('Tags By Hour'),
            column=0,
            order=2
        ))

        self.children.append(TagPopularityChart(
            _('Tag Popularity'),
            column=1,
            order=0
        ))
