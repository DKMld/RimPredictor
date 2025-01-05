from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from RimJobDetection.common import urls as common_urls
from RimJobDetection.accounts import urls as account_urls
from RimJobDetection.predictions import urls as prediction_urls


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(common_urls)),
    path('', include(account_urls)),
    path('', include(prediction_urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
