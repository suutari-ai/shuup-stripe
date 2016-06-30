# -*- coding: utf-8 -*-
# This file is part of Shoop Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from shoop.apps import AppConfig


class ShoopStripeAppConfig(AppConfig):
    name = "shoop_stripe"
    verbose_name = "Shoop Stripe Checkout integration"
    label = "shoop_stripe"
    provides = {
        "front_service_checkout_phase_provider": [
            "shoop_stripe.checkout_phase:StripeCheckoutPhaseProvider",
        ],
        "service_provider_admin_form": [
            "shoop_stripe.admin_forms:StripeCheckoutAdminForm",
        ],
    }


default_app_config = "shoop_stripe.ShoopStripeAppConfig"
