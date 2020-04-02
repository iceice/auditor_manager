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
    url(
        r'add$',
        views.add_student,
    ),
    url(
        r'update$',
        views.update_student,
    ),
    url(
        r'delete$',
        views.delete_student,
    ),
    url(
        r'deletebatch$',
        views.delete_students,
    ),
]
