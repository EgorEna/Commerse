# Generated by Django 3.1.2 on 2020-10-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auctions', '0007_auto_20201030_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(related_name='watcherss', to='auctions.Listing'),
        ),
    ]
