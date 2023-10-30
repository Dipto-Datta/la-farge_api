from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenVerifyView,TokenRefreshView
# create a router and register our viewsets with it
# router.register(r'v1/subject-category-list', views.SubjectCategoryViewSet)

router.register(r'v1/user', user_list_view)
router.register(r'v1/group', group_list_view)
router.register(r'v1/permission', permission_list_view)
urlpatterns = [

    path('', include(router.urls)),


    path('login/', views.login, name='user_login'),
    path('registration/', views.registration, name='user_registration'),
   
    #create superuser
    path('superuser/', views.create_super_user, name='create_super_user'),
    # this endpoint returns- 
    #   status 200 ok and returns "{}", if token is valid 
    #   else throws 401 with error message
    #  TokenVerifyView.as_view()
    # path('token/verify/',  views.token_validation, name='token_verify'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # Todo : CSRF issue resolve
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password/change/', views.change_password, name='change_password'),

    path('logout/', views.logout, name='logout'),


    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




