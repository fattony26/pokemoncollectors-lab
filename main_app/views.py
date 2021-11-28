from django.shortcuts import render
# from .models import Pokemon

class Pokemon: 
  def __init__(self, name, hp, description, age):
    self.name = name
    self.hp = hp
    self.description = description
    self.age = age

pokemons = [
  Pokemon('Pikachu', '9000', 'Abrasive to strangers, and loyal to friends.', 3),
  Pokemon('Squirtle', '150', 'Looks like a turtle.', 0),
  Pokemon('Bulbasaur', '100', 'Loves the jazz cabbage.', 4),
  Pokemon('Charmander', '300', 'Just wants to see the world burn.', 6)
]

def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')
def pokemons_index(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'pokemons/index.html', {'pokemons': pokemons })