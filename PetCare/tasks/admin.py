from django.contrib import admin
from .models import Task, Pet, Personal, Nomina

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

class PetAdmin(admin.ModelAdmin):
    pass

class PersonalAdmin(admin.ModelAdmin):
    pass


class NominaAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Personal,PersonalAdmin)
admin.site.register(Nomina, NominaAdmin)

