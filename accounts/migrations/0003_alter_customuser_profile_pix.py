# Generated by Django 5.0.6 on 2024-07-10 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_profile_pix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pix',
            field=models.ImageField(default='profile_pix/sample.png', upload_to='profile_pix/'),
        ),
    ]
