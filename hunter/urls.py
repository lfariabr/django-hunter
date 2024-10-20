from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from hunter.schema import CustomSchemaGenerator


schema_view = get_schema_view(
   openapi.Info(
      title="Hunter API",
      default_version='v1',
      description="Documentation for usage",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="lfariabr@gmail"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   generator_class=CustomSchemaGenerator,  # Use custom generator here
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Endpoints
    path('api/', include('procedures.urls')),
    path('api/', include('recommendations.urls')),
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')), # new
    
    # Docs
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/hunter/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/hunter/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
