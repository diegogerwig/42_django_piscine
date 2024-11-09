from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import os
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'scripts')
    }),
]
