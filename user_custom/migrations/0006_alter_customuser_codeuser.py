# Generated by Django 5.1.5 on 2025-04-14 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_custom', '0005_job_remove_careerhistory_jobtitle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='codeUser',
            field=models.CharField(default='4a8ced33-d22', max_length=12, unique=True),
        ),
    ]
