# Generated by Django 2.2.6 on 2019-10-26 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20191026_0227'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
    ]
