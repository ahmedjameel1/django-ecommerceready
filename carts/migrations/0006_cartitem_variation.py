# Generated by Django 4.1.1 on 2022-10-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_variations'),
        ('carts', '0005_alter_cart_cart_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, null=True, to='products.variations'),
        ),
    ]
