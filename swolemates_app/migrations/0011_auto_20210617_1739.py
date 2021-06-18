# Generated by Django 2.2 on 2021-06-17 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swolemates_app', '0010_auto_20210617_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend_request',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_requests', to='swolemates_app.User'),
        ),
        migrations.AlterField(
            model_name='friend_request',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to='swolemates_app.User'),
        ),
    ]
