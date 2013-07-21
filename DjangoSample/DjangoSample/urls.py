from django.conf.urls import patterns, include, url
from django.contrib import admin
import  os

admin.autodiscover()
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoSample.views.home', name='home'),
    # url(r'^DjangoSample/', include('DjangoSample.foo.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': PROJECT_PATH + "/DjangoSample/media/"}),
   # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
    