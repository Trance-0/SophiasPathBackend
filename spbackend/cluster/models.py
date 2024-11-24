from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.


def section_file_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to

    A note block can only have one file or image, you need to validate that in form
    """
    return "{0}/{1}/section-{2}/{3}".format(
        instance.page_id.page_type, instance.page_id.slug, instance.slug, filename
    )


class PageTypeChoices(models.TextChoices):
    # this defines the School of philosopher (Set name)
    SCHOOL = "s", _("School")
    # this defines the philosopher (Set name)
    PHILOSOPHER = "p", _("Philosopher")

class Page(models.Model):
    # this defines the School of philosopher (Set name)
    name = models.CharField(max_length=100, unique=True, null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=False)
    page_type = models.CharField(
        max_length=1,
        choices=PageTypeChoices.choices,
        default=PageTypeChoices.PHILOSOPHER,
    )
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class SectionTypeChoices(models.TextChoices):
    # ordinary text
    TEXT = "t", "Text"
    # ordinary image or also used as metadata for the page
    IMAGE = "i", _("Image")
    # ordinary file
    FILE = "f", _("File")
    # This is a note for arrow starting from the current node to the specified [Node] labeled with text in parentheses "Text". There can be cases where an arrow attached with multiple texts. In such case, put texts together on the same arrow.
    FOOTNOTE = "n", _("Footnote")
    # This is the where I add the refence and the link of them.
    READMORE = "r", _("Read More")
    # This is a note for arrow starting from the current node to the specified [Node] labeled with text in parentheses "Text". There can be cases where an arrow attached with multiple texts. In such case, put texts together on the same arrow. the page slug will be stored in args.
    ARROW = "a", _("Arrow")
    # This is the where to add meta data for the entire page
    PAGE_META = "m", _("Page Meta")

class Section(models.Model):
    page_id = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=False,
    )
    subtitle = models.CharField(max_length=100, default="Untitled Section", null=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=False)
    section_type = models.CharField(
        max_length=1,
        choices=SectionTypeChoices.choices,
        default=SectionTypeChoices.TEXT,
    )
    parent_section_id = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # if parent_section_id is not null, this section is a sub-section of parent_section_id
    # if parent_section_id is null, this section is a top-level section
    order = models.IntegerField(default=0, null=False)

    image = models.ImageField(upload_to=section_file_path, blank=True, null=True)
    # file field is currently unsupported
    file = models.FileField(upload_to=section_file_path, blank=True, null=True)

    # unlimited size for PostgreSQL, the max_length value have to be set for other databases.
    text = models.TextField(blank=True, null=True)

    # extra arguments for rendering special features like feature image or coding language
    args = models.CharField(max_length=256, blank=True, null=True)

    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(f"{self.page_id.slug}-{self.subtitle}")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.page_id.name}: {self.subtitle}"
    
class RelationTypeChoices(models.TextChoices):
    # this defines the relation between philosopher and philosopher
    AFFILIATION = "a", _("Affiliation")
    # this defines the relation between philosopher and development
    DEVELOPMENT = "d", _("Development")
    # this defines the relation between philosopher and philosopher
    INFLUENCE = "i", _("Influence")
    # this defines the relation between philosopher and philosopher
    REJECTION = "r", _("Rejection")

class Relation(models.Model):
    # this defines edge for philosopher -> philosopher
    start_page_id = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="outdegree",
        null=False,
    )
    end_page_id = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="indegree",
        null=False,
    )
    relation_type = models.CharField(
        max_length=1,
        choices=RelationTypeChoices.choices,
        default=RelationTypeChoices.AFFILIATION,
    )
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def __str__(self) -> str:
        return f"{self.start_page_id.name} => {self.end_page_id.name}"

class DefinitionLink(models.Model):
    # this class is used to render definition link for the term
    term = models.CharField(max_length=36, null=False)
    definition = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        null=False,
    )

    def __str__(self) -> str:
        return f"{self.term}: {self.definition.subtitle}"


class Tag(models.Model):
    name = models.CharField(max_length=36, null=False)
    slug = models.SlugField(max_length=100, blank=True, null=False)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    section_id = models.ForeignKey(
        Section,
        # when conversation is deleted, whether the creator should also be deleted
        on_delete=models.CASCADE,
        null=False,
    )

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name}: {self.section_id}: {self.section_id.page_id}"
