# Generated by Django 5.0.6 on 2024-07-11 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hira', '0012_customuser_google_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='google_email',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]