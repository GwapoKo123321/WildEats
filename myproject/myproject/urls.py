from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # The correct attribute is admin.site.urls
    path('admin/', admin.site.urls),

    # Requirement 2: Your App Name in the URL
    path('operations/', include('operations.urls')),

    # Root dashboard
    path('', include('operations.urls')),
]