# Generated by Django 3.1.2 on 2020-10-29 23:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auctions', '0004_auto_20201029_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]
