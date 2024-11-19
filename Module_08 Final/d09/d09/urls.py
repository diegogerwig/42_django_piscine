from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
import os
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'account', 'scripts')
    }),
    path('chat/scripts/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'chat', 'scripts')
    }),
    path('', include('account.urls')),  # Account maintains root
    path('chat/', include('chat.urls')),  # Chat under /chat/
]
