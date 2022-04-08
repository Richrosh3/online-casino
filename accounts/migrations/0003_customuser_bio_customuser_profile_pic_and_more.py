# Generated by Django 4.0.3 on 2022-04-07 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_total_added_customuser_total_earnings'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='skill_level',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]