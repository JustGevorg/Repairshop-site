# Generated by Django 3.1.5 on 2021-01-16 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0008_auto_20210115_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='workshop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workshop.workshop', verbose_name='Мастерская'),
        ),
    ]