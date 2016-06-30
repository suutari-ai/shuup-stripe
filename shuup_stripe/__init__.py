# -*- coding: utf-8 -*-
# This file is part of Shuup Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shuup.apps import AppConfig


class ShuupStripeAppConfig(AppConfig):
    name = "shuup_stripe"
    verbose_name = "Shuup Stripe Checkout integration"
    label = "shuup_stripe"
    provides = {
        "front_service_checkout_phase_provider": [
            "shuup_stripe.checkout_phase:StripeCheckoutPhaseProvider",
        ],
        "service_provider_admin_form": [
            "shuup_stripe.admin_forms:StripeCheckoutAdminForm",
        ],
    }


default_app_config = "shuup_stripe.ShuupStripeAppConfig"
