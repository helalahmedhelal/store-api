# Generated by Django 4.2.7 on 2023-12-09 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_front', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='emai',
            new_name='email',
        ),
    ]
