# Generated by Django 5.0.11 on 2025-02-15 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_category_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booksdata',
            old_name='categorie',
            new_name='category',
        ),
    ]
