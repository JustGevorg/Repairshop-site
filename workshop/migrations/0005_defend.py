# Generated by Django 3.1.5 on 2021-01-14 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_auto_20210114_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workshop.guard', verbose_name='Охранная фирма')),
                ('workshop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workshop.workshop', verbose_name='Мастерская')),
            ],
            options={
                'verbose_name': 'Договор с охранной фирмы',
                'verbose_name_plural': 'Договоры с охранными фирмами',
            },
        ),
    ]
