__author__ = 'azurefang'



urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'zheye.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^register$', include(quora.urls))
)
