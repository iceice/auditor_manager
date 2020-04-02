from django.conf.urls import url
from . import views

urlpatterns = [
    url(
        r'show$',
        views.get_students,
    ),
    url(
        r'query$',
        views.query_students,
    ),
    url(
        r'checkID$',
        views.check_studentID,
    ),
]
