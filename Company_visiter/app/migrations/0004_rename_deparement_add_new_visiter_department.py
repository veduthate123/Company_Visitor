# Generated by Django 5.0.2 on 2024-09-09 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_email_add_new_visiter_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='add_new_visiter',
            old_name='deparement',
            new_name='department',
        ),
    ]
