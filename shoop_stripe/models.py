# This file is part of Shoop Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from shoop.core.models import PaymentProcessor, ServiceChoice

from .module import StripeCharger


class StripeCheckoutPaymentProcessor(PaymentProcessor):
    secret_key = models.CharField(max_length=100, verbose_name=_("Secret Key"))
    publishable_key = models.CharField(
        max_length=100, verbose_name=_("Publishable Key"))

    def get_service_choices(self):
        return [ServiceChoice('stripe', _("Stripe Checkout"))]

    def process_payment_return_request(self, service, order, request):
        if not order.is_paid():
            charger = StripeCharger(
                order=order,
                secret_key=self.secret_key
            )
            charger.create_charge()
