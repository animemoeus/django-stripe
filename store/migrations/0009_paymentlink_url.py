# Generated by Django 3.2.20 on 2023-08-23 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_product_stripe_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentlink',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
