# Generated by Django 4.2.2 on 2023-07-23 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_user_bio'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follower', 'followed'), name='follow_unique'),
        ),
    ]