# Generated by Django 5.1.7 on 2025-03-15 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchases',
            old_name='purchases_on',
            new_name='purchased_on',
        ),
    ]
