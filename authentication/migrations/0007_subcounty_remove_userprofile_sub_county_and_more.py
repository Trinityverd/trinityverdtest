# Generated by Django 5.1.7 on 2025-03-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_userprofile_role_alter_userprofile_sub_county'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCounty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_county', models.CharField(choices=[('Kitui East', 'Kitui East'), ('Kitui West', 'Kitui West'), ('Kitui Rural', 'Kitui Rural'), ('Mwingi North', 'Mwingi North'), ('Mwingi Central', 'Mwingi Central'), ('Mbooni West', 'Mbooni West')], max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='sub_county',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sub_county',
            field=models.ManyToManyField(related_name='Supervisor', to='authentication.subcounty'),
        ),
    ]
