# Generated by Django 2.1.5 on 2019-01-13 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='restaurant_id',
            field=models.CharField(default='1', max_length=10),
        ),
    ]
