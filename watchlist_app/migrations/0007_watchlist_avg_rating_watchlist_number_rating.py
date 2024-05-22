# Generated by Django 5.0.6 on 2024-05-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0006_reviews_author"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="avg_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="number_rating",
            field=models.IntegerField(default=0),
        ),
    ]
