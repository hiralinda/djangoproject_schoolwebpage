# Generated by Django 5.0.6 on 2024-07-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hira', '0016_classschedule_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
