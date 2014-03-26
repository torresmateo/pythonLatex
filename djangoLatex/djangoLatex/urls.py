from django.conf.urls import patterns, include, url
import djangoLatex.views as views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
	'',
    # Examples:
    # url(r'^$', 'djangoLatex.views.home', name='home'),
    # url(r'^djangoLatex/', include('djangoLatex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

	url(r'^submit-src/$',views.src_form),
	url(r'^search/$',views.submit),
	url(r'^pdf(.*)$',views.pdf_test),
)
