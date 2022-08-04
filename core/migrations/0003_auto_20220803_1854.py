# Generated by Django 3.2.15 on 2022-08-03 18:54

import annoying.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=annoying.fields.AutoOneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
