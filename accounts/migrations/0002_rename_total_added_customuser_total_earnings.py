# Generated by Django 4.0.3 on 2022-04-06 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='total_added',
            new_name='total_earnings',
        ),
    ]