# Generated by Django 4.2.2 on 2023-07-17 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default='This a bio!', max_length=200),
            preserve_default=False,
        ),
    ]
