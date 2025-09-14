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

    path("accessories/", views.AccessoryListView.as_view(), name="accessory-list"),
    path("accessories/<int:pk>/", views.AccessoryDetailView.as_view(), name="accessory-detail"),
    path("accessories/create/", views.AccessoryCreateView.as_view(), name="accessory-create"),
    path("accessories/<int:pk>/update/", views.AccessoryUpdateView.as_view(), name="accessory-update"),
    path("accessories/<int:pk>/delete/", views.AccessoryDeleteView.as_view(), name="accessory-delete"),

    path('plants/<int:pk>/care/', views.CareActionListView.as_view(), name='careaction-list'),
    path('plants/<int:pk>/care/add/', views.CareActionCreateView.as_view(), name='careaction-add'),
]
