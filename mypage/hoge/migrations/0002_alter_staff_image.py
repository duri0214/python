# Generated by Django 4.0.2 on 2022-02-12 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoge', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='hoge/'),
        ),
    ]