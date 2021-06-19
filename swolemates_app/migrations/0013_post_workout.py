# Generated by Django 2.2 on 2021-06-19 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swolemates_app', '0012_auto_20210617_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='swolemates_app.Workout'),
        ),
    ]
