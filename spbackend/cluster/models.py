from django.db import models

# Create your models here.

def page_file_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to

    A note block can only have one file or image, you need to validate that in form
    """
    return "pages/{1}/{2}".format(
        instance.title, filename
    )

def section_file_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to

    A note block can only have one file or image, you need to validate that in form
    """
    return "pages/{0}/section_{1}/{2}".format(
        instance.page_id.title, instance.subtitle, filename
    )

class Category(models.Model):
    # this defines the category of philosopher (Set name)
    title = models.CharField(max_length=100, default="Untitled Ep", null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

class Development(models.Model):
    # this defines edge for each category
    start_category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="outdegree",
        null=False,
    )
    end_category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="indegree",
        null=False,
    )
    name = models.CharField(max_length=36, unique=True, null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)


class Page(models.Model):
    title = models.CharField(max_length=100, default="Untitled Ep", null=False)
    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=False,
    )
    thumbnail = models.ImageField(upload_to=page_file_path, blank=True, null=True)
    # file field is currently unsupported
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)


class Section(models.Model):
    page_id = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=False,
    )
    subtitle = models.CharField(max_length=100, default="Untitled Sec", null=False)
    image = models.ImageField(upload_to=section_file_path, blank=True, null=True)
    # file field is currently unsupported
    file = models.FileField(upload_to=section_file_path, blank=True, null=True)

    # unlimited size for PostgreSQL, the max_length value have to be set for other databases.
    text = models.TextField(blank=True, null=True)

    # extra arguments for rendering special features like feature image or coding language
    args = models.CharField(max_length=256, null=True)

    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

class Relation(models.Model):
    # this defines edge for each philosopher
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
    name = models.CharField(max_length=36, unique=True, null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

class Tag(models.Model):
    name = models.CharField(max_length=36, unique=True, null=False)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    section_id = models.ForeignKey(
        Section,
        # when conversation is deleted, whether the creator should also be deleted
        on_delete=models.CASCADE,
        null=False,
    )
