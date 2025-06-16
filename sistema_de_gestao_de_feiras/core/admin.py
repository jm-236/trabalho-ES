# core/admin.py

from django.contrib import admin
from .models import Feira, Expositor, Produto

admin.site.register(Feira)
admin.site.register(Expositor)
admin.site.register(Produto)
