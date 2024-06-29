# Generated by Django 4.2 on 2024-06-22 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_user_phone_number_user_full_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('icon', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='latitude',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='favorite_location',
            field=models.ManyToManyField(blank=True, related_name='favorite_location', to='authentication.location'),
        ),
    ]
