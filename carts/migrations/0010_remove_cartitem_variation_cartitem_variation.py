# Generated by Django 4.1.2 on 2022-10-12 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_variations_options_variations_variation_value'),
        ('carts', '0009_alter_cartitem_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='variation',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, null=True, to='products.variations'),
        ),
    ]