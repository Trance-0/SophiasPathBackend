from django.db import models

# Create your models here.

def philosopher_file_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to

    A note block can only have one file or image, you need to validate that in form
    """
    return "Philosophers/{0}/{1}".format(
        instance.title, filename
    )

def section_file_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.FileField.upload_to

    A note block can only have one file or image, you need to validate that in form
    """
    return "Philosophers/{0}/section_{1}/{2}".format(
        instance.Philosopher_id.title, instance.subtitle, filename
    )

class School(models.Model):
    # this defines the School of philosopher (Set name)
    title = models.CharField(max_length=100, default="Unknown School", null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

    def __str__(self) -> str:
        return self.title
    
class Development(models.Model):
    # this defines edge for school -> school
    start_school_id = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="outdegree",
        null=False,
    )
    end_school_id = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="indegree",
        null=False,
    )
    name = models.CharField(max_length=36, null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self) -> str:
        return f"{self.start_school_id.title} => {self.end_school_id.title}"

class Philosopher(models.Model):
    title = models.CharField(max_length=100, default="Unknown Philosopher", null=False)
    school_id = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=False,
    )
    thumbnail = models.ImageField(upload_to=philosopher_file_path, blank=True, null=True)
    # file field is currently unsupported
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)
    
    def __str__(self) -> str:
        return f"{self.school_id.title}:{self.title}"

class Section(models.Model):
    philosopher_id = models.ForeignKey(
        Philosopher,
        on_delete=models.CASCADE,
        null=False,
    )
    subtitle = models.CharField(max_length=100, default="Untitled Section", null=False)
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

    def __str__(self) -> str:
        return f'{self.page_id.title}:{self.subtitle}'

class Relation(models.Model):
    # this defines edge for philosopher -> philosopher
    start_philosopher_id = models.ForeignKey(
        Philosopher,
        on_delete=models.CASCADE,
        related_name="outdegree",
        null=False,
    )
    end_philosopher_id = models.ForeignKey(
        Philosopher,
        on_delete=models.CASCADE,
        related_name="indegree",
        null=False,
    )
    name = models.CharField(max_length=36, null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)
    def __str__(self) -> str:
        return f"{self.start_philosopher_id.title} => {self.end_philosopher_id.title}"

class Affiliation(models.Model):
    # this defines edge for philosopher -> school
    start_philosopher_id = models.ForeignKey(
        Philosopher,
        on_delete=models.CASCADE,
        null=False,
    )
    end_school_id = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=False,
    )
    name = models.CharField(max_length=36, null=False)
    description = models.CharField(max_length=600, blank=True, null=True)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    last_edit = models.DateTimeField(auto_now=True, null=False)

class Tag(models.Model):
    name = models.CharField(max_length=36, null=False)
    # last_use and date_created automatically created, for these field, create one time value to timezone.now()
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    section_id = models.ForeignKey(
        Section,
        # when conversation is deleted, whether the creator should also be deleted
        on_delete=models.CASCADE,
        null=False,
    )

    def __str__(self) -> str:
        return f'{self.name}:{self.section_id}:{self.section_id.philosopher_id}'
