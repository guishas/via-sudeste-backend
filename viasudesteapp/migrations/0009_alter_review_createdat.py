# Generated by Django 4.0.3 on 2022-04-09 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viasudesteapp', '0008_categoria_cliente_notafiscal_pagamento_pedido_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]