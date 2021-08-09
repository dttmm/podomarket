# Generated by Django 2.2 on 2021-08-09 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='kakao_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
