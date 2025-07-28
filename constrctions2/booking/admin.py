from django.contrib import admin
from .models import Booking

# Action to mark selected bookings as paid
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(payment_status='PAID')

mark_as_paid.short_description = "Mark selected bookings as paid"

class BookingAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('user', 'get_project_name', 'payment_status', 'created_at', 'first_instrument_amount', 'second_instrument_amount')  # Added payment amount fields
    
    # Filters to make it easy to filter bookings based on certain criteria
    list_filter = ('payment_status', 'created_at')  # Allow filtering by payment status and creation date
    
    # Search functionality in the admin
    search_fields = ('user__username', 'project__project_name', 'name')  # Search by username, project name, or client name
    
    # Actions in the admin list view (mark as paid)
    actions = [mark_as_paid]  # Add mark_as_paid as a selectable action in the admin panel

    # Method to get the project_name from the related ConstructionProject
    def get_project_name(self, obj):
        return obj.project.project_name
    get_project_name.admin_order_field = 'project_name'  # Allow sorting by project_name in the admin
    get_project_name.short_description = 'Project Name'  # Column title in the admin

admin.site.register(Booking, BookingAdmin)
