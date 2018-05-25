from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
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

    class Media:
        js = ('jet.dashboard/vendor/chart.js/Chart.min.js', 'people/tag_popularity_chart.js')

    def init_with_context(self, context):
        result = people_models.PersonTag.objects.values('tag__value').annotate(tag_count=Count('tag__value'))

        for data in result:
            self.children.append((data['tag__value'], data['tag_count']))

        print(self.children)


class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.available_children.append(TagPopularityChart)

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

        self.children.append(TagPopularityChart(
            _('Tags'),
            column=1,
            order=0
        ))
