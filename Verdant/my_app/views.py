from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import PlantForm, AccessoryForm, CareActionForm
from .models import Plant, Accessory, CareAction



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
    template_name = 'my_app/plants/plant_form.html'
    form_class = PlantForm
    success_url = reverse_lazy('plant-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# Update existing plant
class PlantUpdateView(LoginRequiredMixin, UpdateView):
    model = Plant
    template_name = 'my_app/plants/plant_form.html'
    form_class = PlantForm


# Delete plant
class PlantDeleteView(LoginRequiredMixin, DeleteView):
    model = Plant
    template_name = 'my_app/plants/plant_confirm_delete.html'
    success_url = '/plants/'



# --------------------------
# Accessory Views
# --------------------------

class AccessoryListView(LoginRequiredMixin, ListView):
    model = Accessory
    template_name = "my_app/accessories/accessory_list.html"
    context_object_name = "accessories"


class AccessoryDetailView(LoginRequiredMixin, DetailView):
    model = Accessory
    template_name = "my_app/accessories/accessory_detail.html"

class AccessoryCreateView(LoginRequiredMixin, CreateView):
    model = Accessory
    template_name = "my_app/accessories/accessory_form.html"
    form_class = AccessoryForm
    success_url = reverse_lazy('accessory-list')

class AccessoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Accessory
    template_name = "my_app/accessories/accessory_form.html"
    form_class = AccessoryForm

class AccessoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Accessory
    template_name = "my_app/accessories/accessory_confirm_delete.html"
    success_url = reverse_lazy("accessory-list")



# --------------------------
# CareAction Views
# --------------------------


class CareActionCreateView(LoginRequiredMixin, CreateView):
    model = CareAction
    template_name = 'my_app/careactions/careaction_form.html'
    form_class = CareActionForm

    def form_valid(self, form):
        plant = Plant.objects.get(pk=self.kwargs['pk'])
        form.instance.plant = plant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('plant-detail', args=(self.kwargs['pk'],))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant_id'] = self.kwargs['pk']
        return context


class CareActionListView(LoginRequiredMixin, ListView):
    model = CareAction
    template_name = 'my_app/careactions/careaction_list.html'
    context_object_name = 'care_actions'

    def get_queryset(self):
        self.plant = get_object_or_404(Plant, pk=self.kwargs['pk'])
        return CareAction.objects.filter(plant=self.plant)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant_id'] = self.plant.id 
        context['plant'] = self.plant 
        return context