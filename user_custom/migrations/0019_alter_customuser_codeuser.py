# Generated by Django 5.1.5 on 2025-05-09 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_custom', '0018_alter_customuser_codeuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='codeUser',
            field=models.CharField(default='528170ae-adf', max_length=12, unique=True),
        ),
    ]
