# Generated by Django 4.0.3 on 2022-05-29 16:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('viasudesteapp', '0018_alter_cliente_clientecep_alter_cliente_clientecpf_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='id',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='wishlistId',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
