from django.contrib import admin
from .models import Event, EventImage, Announcement, AnnouncementImage, StotraCategory, Contact, Stotra
from django.utils.text import slugify

# Inline for EventImage
class EventImageInline(admin.TabularInline):  # You can also use StackedInline
    model = EventImage
    extra = 1  # Number of empty image fields to show
    max_num = 10  # Optional: max images allowed per event

# Admin for Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)
    inlines = [EventImageInline]  # Attach inline images

# Optional: still allow EventImage to be editable separately
@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image')
    search_fields = ('event__title',)
    list_filter = ('event__date',)

# Inline for AnnouncementImage
class AnnouncementImageInline(admin.TabularInline):  # You can also use StackedInline   
    model = AnnouncementImage
    extra = 1
    max_num = 10  # Optional: max images allowed per announcement   
# Admin for Announcement
@admin.register(Announcement)   
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)
    inlines = [AnnouncementImageInline]
# Optional: still allow AnnouncementImage to be editable separately
@admin.register(AnnouncementImage)  
class AnnouncementImageAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'image')
    search_fields = ('announcement__title',)
    list_filter = ('announcement__date',)   
# Register your models here.    
# admin.site.register(Event, EventAdmin)
# admin.site.register(EventImage, EventImageAdmin)
# admin.site.register(Announcement, AnnouncementAdmin)
# admin.site.register(AnnouncementImage, AnnouncementImageAdmin)


@admin.register(StotraCategory)
class StotraCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
@admin.register(Stotra)
class StotraAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug')
    search_fields = ('title', 'category__name')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('date_submitted',)
    def subject(self, obj):
        return obj.message[:50] 
    subject.short_description = 'Message Preview'  # Optional: Custom column name   
    def date(self, obj):
        return obj.date_submitted.strftime('%Y-%m-%d %H:%M:%S')
    date.short_description = 'Date Submitted'  # Optional: Custom column name
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('-date_submitted')
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)
        