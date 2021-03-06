# Generated by Django 3.2.7 on 2021-10-29 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to="hotel's_image")),
                ('status', model_utils.fields.StatusField(choices=[('Available', 'Available'), ('Not available', 'Not available')], default='Available', max_length=100, no_check_for_status=True)),
                ('description', models.TextField()),
                ('stars', models.PositiveIntegerField(default=1)),
                ('total_floors', models.PositiveIntegerField(default=1)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('floor', models.PositiveIntegerField(default=1)),
                ('room', model_utils.fields.StatusField(choices=[('single', 'single'), ('double', 'double'), ('triple', 'triple'), ('apartment', 'apartment'), ('suite', 'suite')], default='single', max_length=100, no_check_for_status=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='hotels.hotel')),
            ],
            options={
                'ordering': ['hotel', 'rent'],
            },
        ),
        migrations.CreateModel(
            name='HotelReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('text', models.TextField()),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hotels.hotel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='hotels.hotel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HotelFavorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='hotels.hotel')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
