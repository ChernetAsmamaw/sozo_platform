# Generated by Django 4.2 on 2024-08-31 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_user_comment_name_comment_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='profile',
        ),
    ]