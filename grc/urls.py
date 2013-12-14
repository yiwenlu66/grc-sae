from django.conf.urls import patterns, include, url

urlpatterns = patterns('grc.views',
    url(r'^$', 'Portal'),
    url(r'^review', 'Review'),
    url(r'^about', 'About')
)
