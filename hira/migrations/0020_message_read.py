# Generated by Django 5.0.6 on 2024-07-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hira', '0019_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]