# Generated by Django 2.2.6 on 2019-11-19 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20191115_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Lens', 'Lens'), ('DSLR Camera', 'DSLR Camera'), ('Other Camera', 'Other Camera'), ('Accesory', 'Accesory')], default='DSLR Camera', max_length=13),
        ),
        migrations.AlterField(
            model_name='product',
            name='postcode',
            field=models.PositiveIntegerField(default=2000),
        ),
    ]
