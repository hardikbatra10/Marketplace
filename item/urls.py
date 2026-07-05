from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'item'

router = DefaultRouter()
router.register('items', views.ItemViewSet, basename='item')

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('', include(router.urls)),
]
