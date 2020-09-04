from django.contrib import admin
from django.urls import path, include
from App_Posts import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static


# try to always make the accounts type app under 'accounts'
# and path name 'login' and 'logout'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('App_Login.urls')),
    path('post/',include("App_Posts.urls")),
    path('',views.home,name="home")
    
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)