from django.contrib import admin
from .models import DatosPerson, Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class DatosAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    
admin.site.register(Profile,ProfileAdmin)
admin.site.register(DatosPerson, DatosAdmin)
