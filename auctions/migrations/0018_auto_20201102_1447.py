# Generated by Django 3.1.2 on 2020-11-02 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auctions', '0017_auto_20201102_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='categorie',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='listings',
                                    to='auctions.categorie'),
        ),
    ]
