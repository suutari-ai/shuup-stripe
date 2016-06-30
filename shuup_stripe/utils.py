# -*- coding: utf-8 -*-
# This file is part of Shuup Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

ZERO_DECIMAL_CURRENCIES = (
    # https://support.stripe.com/questions/which-zero-decimal-currencies-does-stripe-support
    "BIF", "CLP", "DJF", "GNF", "JPY", "KMF", "KRW", "MGA",
    "PYG", "RWF", "VND", "VUV", "XAF", "XOF", "XPF"
)


def get_amount_info(amount):
    multiplier = (1 if amount.currency in ZERO_DECIMAL_CURRENCIES else 100)
    return {
        "currency": amount.currency,
        "amount": int(amount.value * multiplier),
    }
