from django.urls import path

from . import views

app_name = 'conversation'

urlpatterns = [
    path('', views.InboxView.as_view(), name='inbox'),
    path('<int:pk>/', views.ConversationDetailView.as_view(), name='detail'),
    path('new/<int:item_pk>/', views.StartConversationView.as_view(), name='new'),
]
