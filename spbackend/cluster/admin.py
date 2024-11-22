import logging
from django.contrib import admin
from django.db.models import Q
from django.utils.text import slugify

# Register your models here.
from .models import DefinitionLink, Page,Section,Relation, SectionTypeChoices,Tag

logger=logging.getLogger(__name__)

class SectionInline(admin.StackedInline):
    """Line per message in admin view and one extra for convenience"""
    model=Section
    ordering=["order"]
    readonly_fields=["date_created","last_edit"]
    extra=1

class PageAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model=Page
    list_display = ("name","page_type","date_created","last_edit",)
    inlines = [
        SectionInline
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        sections=Section.objects.filter(page_id=obj).order_by("order")
        logger.info(f"Checking {len(sections)} sections")
        prev_order=-1
        for section in sections:
            raw_subtitle=section.subtitle
            subtitle=[]
            # correct the order
            if section.order<=prev_order:
                logger.info(f"Correcting order of {section.subtitle}, given {section.order}, prev {prev_order}")
                section.order=prev_order+1
                section.save()
            prev_order=section.order
            # parse the subtitle
            if "[" in raw_subtitle or "]" in raw_subtitle:
                if section.section_type==SectionTypeChoices.ARROW:
                    # TODO: add the page slug to args
                    continue
                # Extract substrings between brackets
                section.subtitle = section.subtitle.replace("[","*[")
                section.subtitle = section.subtitle.replace("]","]*")
                x=section.subtitle.split("*")
                logger.info(f"Splitting subtitle into {x}")
                for i in x:
                    if i.startswith("[") and i.endswith("]"):
                        logger.info(f"Checking if tag {i[1:-1]} exists")
                        if Tag.objects.filter(Q(name=i[1:-1]) & Q(section_id=section)).exists():
                            logger.info(f"Tag {i[1:-1]} already exists")
                            continue
                        tag_instance=Tag.objects.create(name=i[1:-1],section_id=section)
                        logger.info(f"Tag created: {tag_instance}")
                    else:
                        subtitle.append(i)
                section.subtitle=" ".join(subtitle)
                # regenerate slug on change
                section.slug=slugify(section.subtitle)
                section.save()

class RelationAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model=Relation
    list_display = ("name","start_page_id","end_page_id","relation_type","date_created","last_edit",)

# Add model to admin view
admin.site.register(Page,PageAdmin)
admin.site.register(Relation,RelationAdmin)
admin.site.register(DefinitionLink)
admin.site.register(Tag)