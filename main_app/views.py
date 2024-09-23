from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .models import Dog, Toy
from .forms import FeedingForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class Home(LoginView):
  template_name = 'home.html'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def dog_index(request):
  dogs = Dog.objects.filter(user=request.user)
  # You could also retrieve the logged in user's dogs like this
  # dogs = request.user.dog_set.all()
  return render(request, 'dogs/index.html', { 'dogs': dogs })

def dog_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)
  toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'dogs/detail.html', {
    'dog': dog, 'feeding_form': feeding_form, 'toys': toys_dog_doesnt_have
  })

def add_feeding(request, dog_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the dog_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('dog-detail', dog_id=dog_id)

def assoc_toy(request, dog_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('dog-detail', dog_id=dog_id)

class DogCreate(LoginRequiredMixin, CreateView):
  model = Dog
  fields = ['name', 'breed', 'description', 'age']

  def form_valid(self, form):
  # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
  # Let the CreateView do its job as usual
    return super().form_valid(form)

class DogUpdate(UpdateView):
  model = Dog
  fields = ['breed', 'description', 'age']

class DogDelete(DeleteView):
  model = Dog
  success_url = '/dogs/'

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

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
      return redirect('cat-index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  # Same as: return render(request, 'signup.html', {'form': form, 'error_message': error_message})