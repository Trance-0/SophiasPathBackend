# Generated by Django 4.2 on 2024-11-22 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0003_alter_section_parent_section_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]