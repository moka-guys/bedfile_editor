from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BedfileRequest)
admin.site.register(Gene)
admin.site.register(Transcript)