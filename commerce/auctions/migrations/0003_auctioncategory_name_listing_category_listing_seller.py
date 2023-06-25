# Generated by Django 4.2.2 on 2023-06-25 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctioncategory_bid_comment_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctioncategory',
            name='name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='listings', to='auctions.auctioncategory'),
        ),
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
