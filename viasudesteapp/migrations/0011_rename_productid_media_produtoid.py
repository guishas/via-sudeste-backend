# Generated by Django 4.0.3 on 2022-04-10 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viasudesteapp', '0010_media_delete_midia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='productId',
            new_name='produtoId',
        ),
    ]
