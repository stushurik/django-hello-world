from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django_hello_world import settings
from django_hello_world.hello.views import IndexView, ListRequestView, AuthenticationView, \
    UploadFile, DeleteFile, SaveProfile, LoginFormView, UserDataFormView, LogoutView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view(), name='home'),

    url(r'^login/$', LoginFormView.as_view(), name='login'),
    url(r'^login/confirm/$', AuthenticationView.as_view(), name='confirm'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^profile/$', UserDataFormView.as_view(), name='profile'),
    url(r'^profile/upload_file/$', UploadFile.as_view(), name='upload_file'),
    url(r'^profile/delete_file/$', DeleteFile.as_view(), name='delete_file'),
    url(r'^profile/save_profile/$',SaveProfile.as_view(), name='save_profile'),

    # url(r'^django_hello_world/', include('django_hello_world.foo.urls')),
    url(r'^requests/$', ListRequestView.as_view(), name='requests'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns("django.views", url(r"static/(?P<path>.*)$", "static.serve",
                                            {"document_root": settings.STATIC_ROOT}), )
urlpatterns += patterns("django.views", url(r"media/(?P<path>.*)$", "static.serve",
                                            {"document_root": settings.MEDIA_ROOT}), )
