from django.urls import path
from .views import homePageView, processView

urlpatterns = [
    path('', homePageView, name='home'),
    path('process', processView, name='process')
]   