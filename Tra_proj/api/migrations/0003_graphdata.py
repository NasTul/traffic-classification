# Generated by Django 3.1.6 on 2021-02-22 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_graphfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='graphdata',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('graphdata', models.TextField()),
                ('graphname', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'graphdata',
            },
        ),
    ]
