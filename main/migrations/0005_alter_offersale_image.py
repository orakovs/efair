# Generated by Django 4.2.4 on 2023-08-24 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_manufactuter_manufacturer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offersale',
            name='image',
            field=models.ImageField(default='img/no_item_image.jpg', upload_to='img/offer_image'),
        ),
    ]