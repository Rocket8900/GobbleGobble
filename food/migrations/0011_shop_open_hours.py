# Generated by Django 3.2.4 on 2022-04-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20220329_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='open_hours',
            field=models.TextField(default='unknown'),
        ),
    ]