from . import views
from django.urls import path

urlpatterns = [
    path('new/', views.FeedbackListCreate.as_view(), name='feedback-list-create'),
    path('list/', views.FeedbackList.as_view(), name='feedback-detail'),
]