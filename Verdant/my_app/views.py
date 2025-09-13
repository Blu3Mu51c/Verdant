from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Plant

# Home page (login)
class Home(LoginView):
    template_name = 'home.html'

# About page
def about(request):
    return render(request, 'about.html')

# Signup page
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


# --------------------------
# Plant Views
# --------------------------

# List all plants for logged-in user
class PlantListView(LoginRequiredMixin, ListView):
    model = Plant
    template_name = 'my_app/plants/plant_list.html'
    context_object_name = 'plants'

    def get_queryset(self):
        return Plant.objects.filter(owner=self.request.user)


# Plant detail
class PlantDetailView(LoginRequiredMixin, DetailView):
    model = Plant
    template_name = 'my_app/plants/plant-detail.html'
    context_object_name = 'plant'


# Create new plant
class PlantCreateView(LoginRequiredMixin, CreateView):
    model = Plant
    fields = ['name', 'species', 'description', 'growth_stage', 'health', 'accessories']
    template_name = 'my_app/plants/plant_form.html'
    success_url = reverse_lazy('plant-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Update existing plant
class PlantUpdateView(LoginRequiredMixin, UpdateView):
    model = Plant
    template_name = 'my_app/plants/plant_form.html'
    fields = ['name', 'species', 'description', 'growth_stage', 'health', 'accessories']
    success_url = reverse_lazy('plant-list')


# Delete plant
class PlantDeleteView(LoginRequiredMixin, DeleteView):
    model = Plant
    template_name = 'my_app/plants/plant_confirm_delete.html'
    success_url = '/plants/'
