from django.contrib import admin

from .models import Track, Course, Tutor, BlogPost, ContactSubmission


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "track", "price_min", "price_max", "duration", "order")
    list_filter = ("track",)
    list_editable = ("order",)
    search_fields = ("code", "title")


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_founder", "order")
    list_editable = ("order",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published")
    list_filter = ("category", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt")


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "course_interest", "created_at", "handled")
    list_filter = ("handled", "preferred_mode")
    list_editable = ("handled",)
    readonly_fields = ("created_at",)
