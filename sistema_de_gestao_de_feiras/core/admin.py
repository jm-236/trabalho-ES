from django.contrib import admin
from .models import Feira, Expositor, Organizador, Produto, Ingresso

admin.site.register(Feira)
admin.site.register(Expositor)
admin.site.register(Organizador)
admin.site.register(Produto)
admin.site.register(Ingresso)