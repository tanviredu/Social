from django.urls import path
from . import views

app_name = "App_Posts"

urlpatterns = [
    path("",views.home,name="home"),
]
