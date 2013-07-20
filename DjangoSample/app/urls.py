from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from app import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DjangoSample.views.home', name='home'),
    # url(r'^DjangoSample/', include('DjangoSample.foo.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^entry/(?P<entry_id>\d+)/$', views.read, name='read'),
    url(r'^write/$', views.write_form, name='write_form'),
    url(r'^add/post/$', views.add_post),
    url(r'^add/comment/$', views.add_comment),
    url(r'^delete/comment/$', views.delete_comment),
    url(r'^delete/comment/check$', views.delete_comment_check),
    url(r'^get_comments/(?P<entry_id>\d+)/$', views.get_comments),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/', views.logout_page),
    url(r'^register/$', views.register_page),
    url(r'^&', TemplateView.as_view(template_name='/register_success.html')),
    )
