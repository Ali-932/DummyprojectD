from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # Your other URL patterns here...
    path('fetch_objects/', views.fetch_objects, name='fetch_objects'),
]
