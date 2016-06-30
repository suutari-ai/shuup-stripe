# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoop', '0020_services_and_methods'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeCheckoutPaymentProcessor',
            fields=[
                ('paymentprocessor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='shoop.PaymentProcessor')),
                ('secret_key', models.CharField(max_length=100, verbose_name='Secret Key')),
                ('publishable_key', models.CharField(max_length=100, verbose_name='Publishable Key')),
            ],
            options={
                'abstract': False,
            },
            bases=('shoop.paymentprocessor',),
        ),
    ]
