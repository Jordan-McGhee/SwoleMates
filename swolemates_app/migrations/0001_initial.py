# Generated by Django 2.2 on 2021-06-11 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=45, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('profile_photo', models.ImageField(default='default.jpg', upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('friend_requests', models.ManyToManyField(to='swolemates_app.User')),
                ('friends', models.ManyToManyField(related_name='_user_friends_+', to='swolemates_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workouts', to='swolemates_app.User')),
                ('liked_by', models.ManyToManyField(related_name='liked_workouts', to='swolemates_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_by', models.ManyToManyField(related_name='liked_posts', to='swolemates_app.User')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='swolemates_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_count', models.IntegerField()),
                ('rep_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='swolemates_app.Workout')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_by', models.ManyToManyField(related_name='liked_comments', to='swolemates_app.User')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='swolemates_app.Post')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='swolemates_app.User')),
            ],
        ),
    ]
