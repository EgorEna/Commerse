# Generated by Django 3.1.2 on 2020-10-30 17:32

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('auctions', '0008_user_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='master',
            new_name='owner',
        ),
    ]
