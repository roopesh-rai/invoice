# Generated by Django 4.0.3 on 2022-03-24 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_price_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
