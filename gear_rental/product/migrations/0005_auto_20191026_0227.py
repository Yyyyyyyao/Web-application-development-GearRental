# Generated by Django 2.2.6 on 2019-10-26 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='product_pics'),
        ),
    ]
