# Generated by Django 2.2.14 on 2020-07-22 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200722_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='valor-provisorio-slug', max_length=250, unique_for_date='publish'),
            preserve_default=False,
        ),
    ]
