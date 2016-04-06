# This file is part of Shoop Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django import forms
from shoop.admin.forms import ShoopAdminForm

from .models import StripeCheckoutPaymentProcessor


class StripeCheckoutAdminForm(ShoopAdminForm):
    class Meta:
        model = StripeCheckoutPaymentProcessor
        fields = '__all__'
        widgets = {
            'secret_key': forms.PasswordInput(render_value=True),
            'publishable_key': forms.PasswordInput(render_value=True),
        }
