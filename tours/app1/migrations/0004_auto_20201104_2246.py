# Generated by Django 3.1 on 2020-11-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20201104_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
