# Import the admin module from Django
from django.contrib import admin
# Import the models to be registered in the admin panel
from .models import Subject, Course, Module

# Register the Subject model with a custom admin interface
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # Display the title and slug fields in the admin list view
    list_display = ['title', 'slug']
    # Automatically populate the 'slug' field based on the 'title'
    prepopulated_fields = {'slug': ('title',)}


# Inline admin interface to manage modules within a course
class ModuleInline(admin.StackedInline):
    # Specify the model to be included inline
    model = Module


# Register the Course model with a custom admin interface
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ['title', 'subject', 'created']
    # Add filters for 'created' date and 'subject' to refine the list view
    list_filter = ['created', 'subject']
    # Enable searching by 'title' and 'overview' fields
    search_fields = ['title', 'overview']
    # Automatically populate the 'slug' field based on the 'title'
    prepopulated_fields = {'slug': ('title',)}
    # Include the Module model inline within the Course admin view
    inlines = [ModuleInline]
