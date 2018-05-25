from django.urls import path, include
from rest_framework import routers
from people import viewsets


router = routers.DefaultRouter()
router.register(r'persontag', viewsets.PersonTagViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/v1/', include(router.urls)),
]