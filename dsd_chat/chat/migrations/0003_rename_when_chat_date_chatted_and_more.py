# Generated by Django 5.0.1 on 2024-01-08 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_document_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='when',
            new_name='date_chatted',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='uploaded',
            new_name='date_uploaded',
        ),
        migrations.AddField(
            model_name='document',
            name='completed',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]