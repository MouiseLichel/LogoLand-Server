# Generated by Django 2.1.5 on 2019-02-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgsearch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('score', models.FloatField()),
            ],
        ),
    ]