# -*- coding: utf-8 -*-
# This file is part of Shuup Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms


class StripeTokenForm(forms.Form):
    # We're using camel case here only because that's what Stripe does
    stripeToken = forms.CharField(widget=forms.HiddenInput, required=True)
    stripeTokenType = forms.CharField(widget=forms.HiddenInput, required=False)
    stripeEmail = forms.CharField(widget=forms.HiddenInput, required=False)
