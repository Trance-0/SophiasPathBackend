from django.contrib import admin

# Register your models here.
from .models import Category,Development,Page,Section,Relation,Tag

class SectionInline(admin.StackedInline):
    """Line per message in admin view and one extra for convenience"""
    model=Section
    ordering=["date_created"]
    readonly_fields=["date_created","last_edit"]
    extra=1

class PageAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model=Page
    readonly_fields=["date_created","last_edit"]
    inlines = [
        SectionInline
    ]
    extra=1


# Add model to admin view
admin.site.register(Category)
admin.site.register(Development)
admin.site.register(Page,PageAdmin)
admin.site.register(Relation)
admin.site.register(Tag)