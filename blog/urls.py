from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
from . views import *

# app_name = 'blog'
urlpatterns =[
      url(r'^login/$',views.login,name='login'),
      url(r'^logout/$' ,views.logout,name='logout'),
      url(r'^signup/$',signup, name='signup'),
      url(r'^home/$',home,name='home'),
      url(r'^add-keyword/$', add_keyword, name='add_keyword'),
      url(r'^add-code/$', add_code, name='add_code'),
      url(r'^get-profile/$',get_profile,name='get_profile'),
      url(r'^admin/', admin.site.urls),
]


# url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

