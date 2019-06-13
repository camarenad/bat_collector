from django.shortcuts import render, redirect
# Add the following import
from django.http import HttpResponse
from .models import Bat, Toy, Photo
from .forms import FeedingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'batcollect'


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
  toys_bat_doesnt_have = Toy.objects.exclude(id__in = bat.toys.all().values_list('id'))
  feeding_form = FeedingForm()
  return render(request, 'bats/detail.html', {
    'bat': bat, 'feeding_form': feeding_form,
    'toys':  toys_bat_doesnt_have
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

def assoc_toy(request, bat_id, toy_id):
  Bat.objects.get(id=bat_id).toys.add(toy_id)
  return redirect('detail', bat_id=bat_id)

def unassoc_toy(request, bat_id, toy_id):
  Bat.objects.get(id=bat_id).toys.remove(toy_id)
  return redirect('detail', bat_id=bat_id)

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

def add_photo(request, bat_id):
	# photo-file was the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to bat_id or bat (if you have a bat object)
      photo = Photo(url=url, bat_id=bat_id)
      photo.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', bat_id=bat_id)

