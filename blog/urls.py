from django.conf.urls import url
from django.contrib import admin
from .views import *

# app_name = 'blog'
urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^add-keyword/$', add_keyword, name='add_keyword'),
    url(r'^add-code/$', add_code, name='add_code'),
    url(r'^get-profile/$', get_profile, name='get_profile'),
    url(r'^', home, name='home'),
    url(r'^admin/', admin.site.urls),
]

