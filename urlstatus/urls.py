from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from urlstatus.urlstatusapp.views import UrlStatus
from urlstatus.urlstatusapp.mail import Mail
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'urlstatus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^url_status_code/$', url_status_code, name='url_status_code'),
    url(r'^url_status_code/',UrlStatus.as_view()),
    url(r'^mail/$', Mail.as_view(), name='mail')
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
