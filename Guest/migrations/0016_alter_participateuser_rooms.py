# Generated by Django 4.2.3 on 2023-07-07 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0015_participateuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participateuser',
            name='rooms',
            field=models.TextField(default='', max_length=50),
        ),
    ]
