# Generated by Django 3.1.6 on 2021-02-16 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('predictMethods', '0003_user_predict_proba'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='predictMethods.user'),
        ),
    ]
