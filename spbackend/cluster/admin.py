from django.contrib import admin

# Register your models here.
from .models import School,Development,Philosopher,Section,Relation,Affiliation,Tag

class SchoolAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model=School
    list_display = ("name","date_created","last_edit",)

class SectionInline(admin.StackedInline):
    """Line per message in admin view and one extra for convenience"""
    model=Section
    ordering=["date_created"]
    readonly_fields=["date_created","last_edit"]
    extra=1

class PhilosopherAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model=Philosopher
    list_display = ("name","date_created","last_edit",)
    readonly_fields=["date_created","last_edit"]
    inlines = [
        SectionInline
    ]
    extra=1

# Add model to admin view
admin.site.register(School,SchoolAdmin)
admin.site.register(Development)
admin.site.register(Philosopher,PhilosopherAdmin)
admin.site.register(Relation)
admin.site.register(Affiliation)
admin.site.register(Tag)