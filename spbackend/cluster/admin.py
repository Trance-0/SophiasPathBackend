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
    model = Page
    list_display = ("name", "page_type", "date_created", "last_edit",)
    inlines = [
        SectionInline
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Retrieve sections sorted by order (and pk as secondary sort to break ties)
        sections = Section.objects.filter(page_id=obj).order_by("order", "pk")
        logger.info(f"Checking {sections.count()} sections")
        
        # Reassign orders sequentially to ensure unique order values
        for new_order, section in enumerate(sections, start=1):
            raw_subtitle = section.subtitle
            subtitle_parts = []
            # Update order unconditionally if needed
            if section.order != new_order:
                logger.info(f"Updating order of section '{section.subtitle}', from {section.order} to {new_order}")
                section.order = new_order

            # Process subtitle if it contains bracket characters
            if "[" in raw_subtitle or "]" in raw_subtitle:
                if section.section_type == SectionTypeChoices.ARROW:
                    # Skip subtitle processing for ARROW type sections
                    pass
                else:
                    # Insert markers around brackets and split the string
                    modified_subtitle = raw_subtitle.replace("[", "*[").replace("]", "]*")
                    parts = modified_subtitle.split("*")
                    logger.info(f"Splitting subtitle into {parts}")
                    for part in parts:
                        if part.startswith("[") and part.endswith("]"):
                            tag_name = part[1:-1]
                            logger.info(f"Checking if tag '{tag_name}' exists")
                            if Tag.objects.filter(Q(name=tag_name) & Q(section_id=section)).exists():
                                logger.info(f"Tag '{tag_name}' already exists")
                            else:
                                tag_instance = Tag.objects.create(name=tag_name, section_id=section)
                                logger.info(f"Tag created: {tag_instance}")
                        else:
                            subtitle_parts.append(part)
                    # Regenerate the subtitle and slug based on processed parts
                    new_subtitle = " ".join(subtitle_parts).strip()
                    section.subtitle = new_subtitle
                    section.slug = slugify(new_subtitle)
            section.save()

class RelationAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model=Relation
    list_display = ("start_page_id","relation_type","end_page_id","date_created","last_edit")

# Add model to admin view
admin.site.register(Page,PageAdmin)
admin.site.register(Relation,RelationAdmin)
admin.site.register(DefinitionLink)
admin.site.register(Tag)