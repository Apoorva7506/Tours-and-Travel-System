# Generated by Django 3.1 on 2020-11-04 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20201104_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='locality',
        ),
        migrations.AddField(
            model_name='destination',
            name='info',
            field=models.TextField(default='something'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='hpic',
            field=models.ImageField(blank=True, default='media/h.jpg', upload_to='hotel/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='info',
            field=models.TextField(default='Something'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='package',
            name='ppic',
            field=models.ImageField(blank=True, default='media/h.jpg', upload_to='package/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='popularspots',
            name='popic',
            field=models.ImageField(blank=True, default='media/h.jpg', upload_to='pop/%Y/%m/%d/'),
        ),
    ]
