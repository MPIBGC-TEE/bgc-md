# Generated by Django 2.0.6 on 2018-06-18 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yaml_creator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleFlux',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doi', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]