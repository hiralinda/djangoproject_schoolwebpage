# Generated by Django 5.0.6 on 2024-07-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hira', '0017_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
