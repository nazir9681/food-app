# Generated by Django 3.0.8 on 2020-09-10 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='firebasenotification',
            name='status',
            field=models.CharField(choices=[('1', 'ACTIVE'), ('0', 'INACIVE')], default='1', max_length=1),
        ),
    ]
