# Generated by Django 4.2.3 on 2023-09-08 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organizer', '0006_event_tot_capacity_alter_event_rooms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatecodes',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
