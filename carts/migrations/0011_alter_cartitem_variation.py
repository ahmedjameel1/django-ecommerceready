# Generated by Django 4.1.2 on 2022-10-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_variations_options_variations_variation_value'),
        ('carts', '0010_remove_cartitem_variation_cartitem_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='products.variations'),
        ),
    ]
