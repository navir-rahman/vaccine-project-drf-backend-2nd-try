from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()    
router.register('all_vaccine', views.VaccineViewSet) 
router.register('history', views.VaccineRecordViewSet) 
urlpatterns = [
    path('', include(router.urls)),
    path('add', views.AddVaccineViewSet.as_view() ),
    # path('order/<int:id>/', views.order_vaccine.as_view() ),
    path('delete/<int:pk>/', views.VaccineDeleteAPIView.as_view(), name='vaccine-delete'),
    
] 