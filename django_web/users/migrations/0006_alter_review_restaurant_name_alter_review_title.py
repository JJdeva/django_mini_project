# Generated by Django 4.0 on 2022-11-22 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='restaurant_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]
