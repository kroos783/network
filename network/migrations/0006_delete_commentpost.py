# Generated by Django 3.2.7 on 2021-12-09 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_followuser_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CommentPost',
        ),
    ]