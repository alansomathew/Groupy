# Generated by Django 4.2.3 on 2023-09-08 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Organizer', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='PrivateCodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('status', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizer.event')),
            ],
        ),
    ]
