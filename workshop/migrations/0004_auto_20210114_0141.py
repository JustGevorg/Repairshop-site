# Generated by Django 3.1.5 on 2021-01-13 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0003_auto_20210114_0126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('status', models.CharField(max_length=50, verbose_name='Репутация')),
            ],
            options={
                'verbose_name': 'Охранная фирма',
                'verbose_name_plural': 'Охранные фирмы',
            },
        ),
        migrations.DeleteModel(
            name='Tool',
        ),
    ]