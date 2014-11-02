from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'djrt.views.home', name='home'),
    # url(r'^djrt/', include('djrt.foo.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^show_ticket/(\d+)/$', 'webapp.views.show_ticket'),
    # url(r'^ct/$', 'webapp.views.cookies_test'),
    url(r'^addt/$', 'webapp.views.add_ticket'),
    url(r'^addc/(\d+)/$', 'webapp.views.add_comment'),
    url(r'^login/$', 'webapp.views.login'),
    url(r'^logout/$', 'webapp.views.logout'),
    url(r'^$', 'webapp.views.index'),
    url(r'^reg/$', 'webapp.views.registration'),
    url(r'^message/$', 'webapp.views.message'),
    url(r'^settings/$', 'webapp.views.user_settings'),
)
