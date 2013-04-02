from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('tsj_app.views',
    url(r'^$', 'index', name='index'),
    url(r'^login/$', login, kwargs=dict(template_name='login.html'),
        name='login'),
    url(r'^logout/$', logout, kwargs=dict(next_page='/'),
        name='logout'),
)
