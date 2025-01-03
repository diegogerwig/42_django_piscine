from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

# Base URLpatterns (without language prefix)
urlpatterns = [
    path('', RedirectView.as_view(url='/articles/', permanent=False)),
    path('i18n/', include('django.conf.urls.i18n')),
    path('articles/', include('ex.urls')),  # No-prefix URL
]

# i18n patterns (with language prefix)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('articles/', include('ex.urls')),
    prefix_default_language=True  # This ensures both /en/ and /es/ URLs work
)
