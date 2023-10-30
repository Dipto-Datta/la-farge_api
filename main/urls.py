"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

#swagger config
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#swagger views settings

schema_view = get_schema_view(
   openapi.Info(
    title="Swagger with django API",
    default_version='v1',
    description="powered by spaceyatech and Tamarcom Technology",
    terms_of_service="https://www.ourapp.com/policies/terms/",
    contact=openapi.Contact(email="contact@expense.local"),
    license=openapi.License(name="Test License"),),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [

    path('admin/', admin.site.urls),
     # for swagger ui
    path ('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # auth urls --only for authentication and authorization purpose
    path("auth/",include('core.urls')),
    
    # app urls -- /api/appname/ -- for general apps
   


    
]
