# Generated by Django 4.0.3 on 2022-04-06 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GradingSystem', '0003_usersreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactName', models.CharField(max_length=254)),
                ('contactEmail', models.EmailField(max_length=254)),
                ('contactSubject', models.CharField(max_length=254)),
                ('contactMessage', models.TextField()),
            ],
        ),
    ]
