# Generated by Django 4.2.1 on 2023-06-09 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_scraper', '0009_alter_doctor_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='services',
            field=models.CharField(blank=True, max_length=20000, null=True),
        ),
    ]
