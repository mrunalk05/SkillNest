# Generated by Django 4.1.4 on 2023-01-06 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skillex', models.IntegerField()),
                ('skilllevel', models.CharField(max_length=100)),
                ('project', models.TextField()),
            ],
        ),
    ]