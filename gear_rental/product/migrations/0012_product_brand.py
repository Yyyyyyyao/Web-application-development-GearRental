# Generated by Django 2.2.6 on 2019-11-01 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20191101_0356'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('Nikon', 'Nikon'), ('Canon', 'Canon'), ('Sony', 'Sony'), ('Casio', 'Casio'), ('Panasonic', 'Panasonic'), ('Pentax', 'Pentax'), ('Lumix', 'Lumix'), ('GoPro', 'GoPro'), ('Olympus', 'Olympus'), ('Other Brand', 'Other Brand')], default='Other Brand', max_length=11),
        ),
    ]
