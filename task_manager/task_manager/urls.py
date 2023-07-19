from django.contrib import admin
from django.urls import path, include
# from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_swagger_view(title='Your API Documentation')


schema_view = get_schema_view(
    openapi.Info(
        title="Task Management API Documentation",
        default_version='v1',
        description="API documentation for your project",
        terms_of_service="https://your-terms-of-service-url/",
        contact=openapi.Contact(email="armanicepust9@gmail.com"),
        license=openapi.License(name="DSF License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('task_manager_app.urls')),
    
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
