# Generated by Django 5.0.11 on 2025-01-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksdata',
            name='book_title',
            field=models.SlugField(blank=True, db_collation='Hebrew_CI_AS', max_length=150, null=True),
        ),
    ]
