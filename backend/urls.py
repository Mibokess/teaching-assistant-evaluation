"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .api.views import index_view
from .api.views import CSVViewSet
from .api.views import LectureViewSet
from .api.views import QuestionViewSet
from .api.views import SessionViewSet
from .api.views import TeachingAssistantViewSet
from .api.views import VoteViewSet
from .api.views import login_view

router = routers.DefaultRouter()

router.register('lectures', LectureViewSet)
router.register('questions', QuestionViewSet)
router.register('sessions', SessionViewSet)
router.register('tas', TeachingAssistantViewSet)
router.register('votes', VoteViewSet)
router.register('upload', CSVViewSet, base_name='upload')

admin.site.site_header = 'TA+ Evaluation Tool - Administration Page'

urlpatterns = [

    # http://localhost:8000/
    path('', index_view, name='index'),

    # http://localhost:8000/api/<router-viewsets>
    path('api/', include(router.urls)),

    # http://localhost:8000/api/admin/
    path('api/admin/', admin.site.urls),

    path('api/login/', login_view)
]


