# Generated by Django 4.2 on 2024-11-22 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_alter_section_section_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='parent_section_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cluster.section'),
        ),
        migrations.AlterField(
            model_name='section',
            name='section_type',
            field=models.CharField(choices=[('t', 'Text'), ('i', 'Image'), ('f', 'File'), ('n', 'Footnote'), ('r', 'Read More'), ('m', 'Page Meta')], default='t', max_length=1),
        ),
    ]