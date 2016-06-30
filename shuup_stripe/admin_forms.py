# This file is part of Shuup Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django import forms
from shuup.admin.forms import ShuupAdminForm

from .models import StripeCheckoutPaymentProcessor


class StripeCheckoutAdminForm(ShuupAdminForm):
    class Meta:
        model = StripeCheckoutPaymentProcessor
        fields = '__all__'
        widgets = {
            'secret_key': forms.PasswordInput(render_value=True),
            'publishable_key': forms.PasswordInput(render_value=True),
        }
