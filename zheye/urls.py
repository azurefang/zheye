from django.conf.urls import patterns, include, url

from django.contrib import admin
from quora.views import *
from ajax.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zheye.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^register$', register),
    url(r'^login$', user_login),
    url(r'^people/(?P<aDomain>(\w+\-)*\w+)', display_account),
    url(r'^topic/(?P<tId>\w+)', display_topic),
    url(r'^ask_question/', ask_question),
    url(r'^question/(?P<qId>\w+)', display_question),
    url(r'^topic$', followed_topics),
    url(r'^topics$', show_topics),
    url(r'^static_media/(?P<path>.*)','django.views.static.serve',{'document_root':'./media/'}),
    url(r'^ajax/topic', ajax_topic_json)
)
