from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    # Admin urls
    path('admin/', admin.site.urls),

    # API urls
    path('api/v1/', include('api.urls')),

    # Redoc
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
