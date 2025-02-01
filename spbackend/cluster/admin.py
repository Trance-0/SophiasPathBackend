import logging
from django.contrib import admin
from django.db.models import Q
from django.utils.text import slugify

from django.core.exceptions import ValidationError

import re
# add custom form for fast upload
from django import forms

# Register your models here.
from .models import DefinitionLink, Page, Section, Relation, SectionTypeChoices, Tag

logger = logging.getLogger(__name__)

class SectionInline(admin.StackedInline):
    """Line per message in admin view and one extra for convenience"""
    model = Section
    ordering = ["order"]
    readonly_fields = ["date_created", "last_edit"]
    extra = 1

class PageAdminForm(forms.ModelForm):
    fast_upload = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text="Paste full markdown file for fast section upload. WARNING: This will delete all existing sections and create new ones from the uploaded markdown."
    )

    class Meta:
        model = Page
        fields = ["name", "slug", "page_type", "description", "fast_upload"]

class PageAdmin(admin.ModelAdmin):
    """Admin view for Page with fast_upload field included."""
    form = PageAdminForm
    model = Page
    inlines = [SectionInline]
    readonly_fields = ["date_created", "last_edit"]


    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)

            # Process fast_upload field if provided: parse markdown into sections.
            fast_upload = form.cleaned_data.get("fast_upload")
            if fast_upload:
                # clean up all the sections except the meta section
                Section.objects.filter(page_id=obj).exclude(section_type=SectionTypeChoices.PAGE_META).delete()
                logger.info("Cleaned up all sections except the meta section")
                heading_matches = list(re.finditer(r'^(#{1,6})\s+(.*)$', fast_upload, re.MULTILINE))
                logger.info(f"Found {len(heading_matches)} headings in fast upload")
                created_sections = []  # track created sections for potential rollback
                section_stack = []  # stack of tuples: (header level, Section instance)

                for i, match in enumerate(heading_matches):
                    hashes = match.group(1)
                    title = match.group(2)
                    level = len(hashes)
                    # Extract text content after the header until the next header (or end of file)
                    if i + 1 < len(heading_matches):
                        text_content = fast_upload[match.end():heading_matches[i + 1].start()].strip()
                    else:
                        text_content = fast_upload[match.end():].strip()

                    if level in [1, 2]:
                        # For level 1 and 2, always no parent.
                        parent_section = None
                        # Clean the stack of any sections at this level or deeper.
                        while section_stack and section_stack[-1][0] >= level:
                            section_stack.pop()
                    else:
                        # For headers of level 3 and deeper, find a parent with level exactly one less.
                        while section_stack and section_stack[-1][0] >= level:
                            section_stack.pop()
                        if not section_stack or section_stack[-1][0] != level - 1:
                            error_message = f"Header level mismatch: '{hashes} {title}' does not follow a valid parent header."
                            # Rollback: delete all sections created from fast_upload
                            Section.objects.filter(id__in=[s.id for _, s in created_sections]).delete()
                            logger.error(error_message)
                            raise ValidationError(error_message)
                        parent_section = section_stack[-1][1]

                    # select section type based on title
                    section_type = SectionTypeChoices.TEXT
                    if any(keyword in title.lower() for keyword in ["reference", "read more", "readmore"]):
                        section_type = SectionTypeChoices.READMORE
                    elif any(keyword in title.lower() for keyword in ["arrow to"]):
                        section_type = SectionTypeChoices.ARROW
                    elif any(keyword in title.lower() for keyword in ["footnotes", "footnote"]):
                        section_type = SectionTypeChoices.FOOTNOTE



                    # obsolete types
                    elif "Image" in title:
                        section_type = SectionTypeChoices.IMAGE
                    elif "File" in title:
                        section_type = SectionTypeChoices.FILE
                        

                    new_section = Section(
                        page_id=obj,
                        subtitle=title.strip(),
                        order=i + 1,  # Temporary order; will be reassigned below.
                        section_type=section_type,
                        slug=slugify(f"{obj.slug}-{title}"),
                        parent_section_id=parent_section,
                        text=text_content
                    )
                    new_section.save()
                    created_sections.append((level, new_section))
                    section_stack.append((level, new_section))
                    logger.info(f"Created section from fast upload: '{title}' with level {level}")


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
                        relate_to, relation_name = re.match(r'Arrow to \[(.*)\]\s+\("(.*)"\)', raw_subtitle).groups()
                        # check existing definition links
                        definition_links = DefinitionLink.objects.filter(term=relate_to).first()
                        if definition_links is None:
                            logger.warning(f"Definition link for '{relate_to}' not found, please create the link in the definition link section.")
                        else:
                            logger.info(f"Definition link for '{relate_to}' already exists, adding relation to '{relation_name}'")
                            section.args = definition_links.url()
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
        except Exception as e:
            logger.exception("An error occurred while saving the Page model.")
            from django.contrib import messages
            messages.error(request, f"An error occurred: {e}")
            # Optionally, you could rollback changes or perform additional error handling here.

class RelationAdmin(admin.ModelAdmin):
    """ in admin view and one extra for convenience"""
    model = Relation
    list_display = ("start_page_id", "relation_type", "end_page_id", "date_created", "last_edit")

# Add model to admin view
admin.site.register(Page, PageAdmin)
admin.site.register(Relation, RelationAdmin)
admin.site.register(DefinitionLink)
admin.site.register(Tag)