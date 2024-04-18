from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter() # amader router

router.register('user', views.UserViewSet) # router er antena
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginApiView.as_view(), name='login'),
    path('register/', views.UserRegistrationApiView.as_view(), name='register'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileViewSet.as_view(), name = 'profile'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
]