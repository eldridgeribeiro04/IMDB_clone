# Generated by Django 5.0.6 on 2024-05-16 22:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0003_streamplatform_watchlist_delete_movie"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="platform",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlist",
                to="watchlist_app.streamplatform",
            ),
            preserve_default=False,
        ),
    ]
