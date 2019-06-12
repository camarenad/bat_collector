from django.shortcuts import render, redirect
# Add the following import
from django.http import HttpResponse
from .models import Bat
from .forms import FeedingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Define the home view
def home(request):
  return HttpResponse('<h1>Hello /ᐠ｡‸｡ᐟ\ﾉ</h1>')

def about(request):
  return render(request, 'about.html')

def bats_index(request):
  bats = Bat.objects.all()
  return render(request, 'bats/index.html', {'bats': bats})


def bats_detail(request, bat_id):
  bat = Bat.objects.get(id=bat_id)
  feeding_form = FeedingForm()
  return render(request, 'bats/detail.html', {
    'bat': bat, 'feeding_form': feeding_form
  })


class BatCreate(CreateView):
  model = Bat
  fields = '__all__'
  success_url = '/bats/'

class BatUpdate(UpdateView):
  model = Bat
  fields = ['breed','description','age']

class BatDelete(DeleteView):
  model = Bat
  success_url = '/bats/'

def add_feeding(request,bat_id):
  form = FeedingForm(request.POST)
  if form.is_valid():
    new_feeding = form.save(commit=False)
    new_feeding.bat_id = bat_id
    new_feeding.save()

  return redirect('detail', bat_id=bat_id)

