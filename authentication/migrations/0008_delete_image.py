# Generated by Django 4.0.3 on 2022-05-10 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_image_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]
