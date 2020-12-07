# Generated by Django 3.1.3 on 2020-12-06 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0006_auto_20201124_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drive',
            old_name='discounted_charge',
            new_name='charge_discount',
        ),
        migrations.AddField(
            model_name='drive',
            name='safety_discount',
            field=models.IntegerField(default=0),
        ),
    ]