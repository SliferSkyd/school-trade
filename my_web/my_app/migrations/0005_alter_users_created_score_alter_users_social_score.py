# Generated by Django 5.2 on 2025-05-13 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_participateform_donated_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='created_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='social_score',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
