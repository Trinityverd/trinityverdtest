# Generated by Django 5.1.7 on 2025-03-13 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_subcounty_remove_userprofile_sub_county_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcounty',
            name='sub_county',
            field=models.CharField(max_length=100),
        ),
    ]
