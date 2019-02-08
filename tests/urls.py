from django.conf.urls import include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^cookies/', include('cookie_consent.urls')),
    re_path(r'', include('core.urls')),
]

urlpatterns += staticfiles_urlpatterns()
