from django.contrib import admin
from .models import AssessorProfile
from .forms import AssessorProfileForm
from .models import AssessmentReports
from django.utils.html import format_html
from django.urls import reverse
from .models import AssessmentReports

class AssessorProfileAdmin(admin.ModelAdmin):
    form = AssessorProfileForm
    list_display = ['names', 'id_number', 'username']

admin.site.register(AssessorProfile, AssessorProfileAdmin)


@admin.register(AssessmentReports)
class AssessmentReportsAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at', 'view_files_link')

    def view_files_link(self, obj):
        url = reverse('admin_uploaded_files')  # Make sure the name matches your URL pattern
        return format_html('<a class="button" href="{}">View Uploaded Files</a>', url)

    view_files_link.short_description = 'Uploaded Files'
    view_files_link.allow_tags = True