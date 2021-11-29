from django.shortcuts import render, redirect
from .models import Pokemon, Toy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class PokemonCreate(LoginRequiredMixin, CreateView):
  model = Pokemon
  fields = ['name', 'hp', 'description', 'age']
  success_url = '/pokemons/'
class PokemonUpdate(LoginRequiredMixin, UpdateView):
  model = Pokemon
  fields = ['hp', 'description', 'age']
class PokemonDelete(LoginRequiredMixin, DeleteView):
  model = Pokemon
  success_url = '/pokemons/'
class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'
class ToyList(LoginRequiredMixin, ListView):
  model = Toy
class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy
class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']
class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'
class Home(LoginView):
  template_name = 'home.html'

def about(request):
  return render(request, 'about.html')

@login_required
def pokemons_index(request):
  pokemons = Pokemon.objects.filter(user=request.user)
  return render(request, 'pokemons/index.html', {
    'pokemons': pokemons
  })

def pokemons_detail(request, pokemon_id):
  pokemon = Pokemon.objects.get(id=pokemon_id)
  toys_pokemon_doesnt_have = Toy.objects.exclude(id__in = pokemon.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'pokemons/detail.html', {
    'pokemon': pokemon, 
    'feeding_form': feeding_form, 
    'toys': toys_pokemon_doesnt_have
  })

def add_feeding(request, pokemon_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.pokemon_id = pokemon_id
    new_feeding.save()
  return redirect('pokemons_detail', pokemon_id=pokemon_id)

def assoc_toy(request, pokemon_id, toy_id):
  Pokemon.objects.get(id=pokemon_id).toys.add(toy_id)
  return redirect('pokemons_detail', pokemon_id=pokemon_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('pokemons_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)