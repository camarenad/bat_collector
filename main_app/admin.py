from django.contrib import admin

# Register your models here.
from .models import Bat, Feeding, Toy

admin.site.register(Bat)
admin.site.register(Feeding)
admin.site.register(Toy)

