# Generated by Django 4.2.1 on 2023-06-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_scraper', '0007_remove_doctor_review_review_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='sub_specialty',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]