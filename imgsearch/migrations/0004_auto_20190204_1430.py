# Generated by Django 2.1.5 on 2019-02-04 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imgsearch', '0003_auto_20190204_1409'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='imageSearch',
            new_name='image_search',
        ),
    ]
