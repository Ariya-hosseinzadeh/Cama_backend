# Generated by Django 5.1.5 on 2025-05-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_custom', '0022_alter_customuser_codeuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='codeUser',
            field=models.CharField(default='3bf7735a-cd8', max_length=12, unique=True),
        ),
    ]
