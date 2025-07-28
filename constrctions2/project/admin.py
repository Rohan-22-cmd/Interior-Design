from django.contrib import admin
from .models import ConstructionProject
admin.site.register(ConstructionProject)
# @admin.register(ConstructionProject)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('project_name', ' start_date', ' end_date', 'location','  budget','client_name')
#     search_fields = ('project_name')
