# Generated by Django 5.1.5 on 2025-05-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Topics', '0002_remove_post_edited_at_remove_post_is_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, unique=True),
        ),
    ]
