from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('student_consent', views.student_consent, name='student_consent'),
    path('assessment', views.assessment, name='assessment'),
    path('assessment_end', views.assessment_end, name='assessment_end'),
    # path('marker', views.marker_index, name='marker_index'),
    # path('marker_consent', views.marker_consent, name='marker_consent'),
    # path('marking', views.marking, name='marking'),
]