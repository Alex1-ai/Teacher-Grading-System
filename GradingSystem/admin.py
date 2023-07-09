

# Register your models here.
from django.contrib import admin
from .models import User
from . import models
# Register your models here.

admin.site.site_header = 'Grading System Admin'
admin.site.index_title = 'Admin'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'mobile', ]


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['contactName', 'contactEmail',
                    'contactSubject', 'contactMessage' ]


@admin.register(models.Faculties)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['facultyName', 'facultyDesc']


@admin.register(models.UsersReview)
class usersReviewAdmin(admin.ModelAdmin):
    list_display = ['lecturerName', 'lecturerCourse', 'courseCode',
                    'communicationSkills', 'listeningSkills', 'userReview']
