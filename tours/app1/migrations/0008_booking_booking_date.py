# Generated by Django 2.2.10 on 2020-11-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_remove_mot_ac_nac'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
