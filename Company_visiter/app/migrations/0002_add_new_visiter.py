# Generated by Django 5.0.2 on 2024-09-09 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_new_visiter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=50)),
                ('Email', models.CharField(max_length=50)),
                ('phonenum', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('whomtomeet', models.CharField(max_length=50)),
                ('deparement', models.CharField(max_length=50)),
                ('reasontomeet', models.CharField(max_length=50)),
            ],
        ),
    ]
