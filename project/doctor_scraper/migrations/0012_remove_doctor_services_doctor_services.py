# Generated by Django 4.2.1 on 2023-06-09 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_scraper', '0011_alter_doctor_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='services',
        ),
        migrations.AddField(
            model_name='doctor',
            name='services',
            field=models.ManyToManyField(to='doctor_scraper.services'),
        ),
    ]
