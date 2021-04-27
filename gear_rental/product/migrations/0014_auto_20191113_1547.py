# Generated by Django 2.2.7 on 2019-11-13 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_merge_20191113_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Lence', 'Lence'), ('DSLR Camera', 'DSLR Camera'), ('Other Camera', 'Other Camera'), ('Accesory', 'Accesory')], default='DSLR Camera', max_length=11),
        ),
        migrations.AlterField(
            model_name='product',
            name='postcode',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
