from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from user.views import RegisterView

urlpatterns = [
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(),
         name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('base-auth/', include('rest_framework.urls')),
    path('register/', RegisterView.as_view(), name='auth_register'),
]