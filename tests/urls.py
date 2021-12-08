from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cookies/', include('cookie_consent.urls')),
    path('', include('core.urls')),
]

urlpatterns += staticfiles_urlpatterns()
