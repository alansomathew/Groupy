# Generated by Django 4.2.2 on 2023-06-15 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Guest', '0001_initial'),
        ('Organizer', '0002_remove_room_events_delete_event_delete_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('rooms', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.organiser')),
            ],
        ),
        migrations.CreateModel(
            name='room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50)),
                ('capacity', models.IntegerField(default=0)),
                ('events', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizer.event')),
            ],
        ),
    ]
