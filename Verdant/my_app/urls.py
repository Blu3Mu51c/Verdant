from django.urls import path
from . import views

urlpatterns = [
    # Home, About, Signup
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),

    # Plants CRUD
    path('plants/', views.PlantListView.as_view(), name='plant-list'),
    path('plants/<int:pk>/', views.PlantDetailView.as_view(), name='plant-detail'),
    path('plants/create/', views.PlantCreateView.as_view(), name='plant-create'),
    path('plants/<int:pk>/update/', views.PlantUpdateView.as_view(), name='plant-update'),
    path('plants/<int:pk>/delete/', views.PlantDeleteView.as_view(), name='plant-delete'),
]
