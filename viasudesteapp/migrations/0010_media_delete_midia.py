# Generated by Django 4.0.3 on 2022-04-10 21:31

from django.db import migrations, models
import viasudesteapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('viasudesteapp', '0009_alter_review_createdat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productId', models.CharField(max_length=200)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to=viasudesteapp.models.upload_product_image)),
            ],
        ),
        migrations.DeleteModel(
            name='Midia',
        ),
    ]
