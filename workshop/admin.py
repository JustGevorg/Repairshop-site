from django.contrib import admin

from .models import Workshop, Guard, Master, WorksOn, Defend, Review, AdminRequest


# Register your models here.


admin.site.register(Workshop)
admin.site.register(Guard)
admin.site.register(Master)
admin.site.register(WorksOn)
admin.site.register(Defend)
admin.site.register(Review)
admin.site.register(AdminRequest)
