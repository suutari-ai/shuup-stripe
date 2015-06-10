# -*- coding: utf-8 -*-
# This file is part of Shoop.
#
# Copyright (c) 2012-2015, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.timezone import now
import os

import pytest
from shoop.front.basket import get_basket
from shoop.utils.excs import Problem
from shoop_tests.utils import printable_gibberish, apply_request_middleware
from shoop_stripe.checkout_phase import StripeCheckoutPhase
from shoop_stripe.module import StripeCheckoutModule
from shoop.testing.factories import (
    get_default_product,
    get_default_supplier,
    create_order_with_product,
    get_default_shop)
from shoop.utils.http import retry_request


@pytest.fixture
def stripe_payment_module():
    sk = os.environ.get("STRIPE_SECRET_KEY")
    if not sk:
        pytest.skip("Can't test Stripe without STRIPE_SECRET_KEY envvar")
    return StripeCheckoutModule(None, {
        "publishable_key": "x",
        "secret_key": sk
    })


def _create_order_for_stripe():
    product = get_default_product()
    supplier = get_default_supplier()
    order = create_order_with_product(
        product=product, supplier=supplier, quantity=1,
        taxless_unit_price=100, tax_rate=0
    )
    order.cache_prices()
    assert order.taxless_total_price > 0
    if not order.payment_data:
        order.payment_data = {}
    order.save()
    return order


def get_stripe_token(stripe_payment_module):
    return retry_request(
        method="post",
        url="https://api.stripe.com/v1/tokens",
        auth=(stripe_payment_module.options["secret_key"], "x"),
        data={
            "card[number]": "4242424242424242",
            "card[exp_month]": 12,
            "card[exp_year]": now().date().year + 1,
            "card[cvc]": 666,
        }
    ).json()


##############################################################################

@pytest.mark.django_db
def test_stripe_basics(rf, stripe_payment_module):
    """
    :type rf: RequestFactory
    :type stripe_payment_module: StripeCheckoutModule
    """
    order = _create_order_for_stripe()
    token = get_stripe_token(stripe_payment_module)
    token_id = token["id"]
    order.payment_data["stripe"] = {"token": token_id}
    order.save()
    stripe_payment_module.process_payment_return_request(order, rf.post("/"))
    assert order.is_paid()
    assert order.payments.first().payment_identifier.startswith("Stripe-")


@pytest.mark.django_db
def test_stripe_bogus_data_fails(rf, stripe_payment_module):
    order = _create_order_for_stripe()
    order.payment_data["stripe"] = {"token": printable_gibberish(30)}
    order.save()
    with pytest.raises(Problem):
        stripe_payment_module.process_payment_return_request(
            order,
            rf.post("/")
        )


@pytest.mark.django_db
def test_stripe_checkout_phase(rf, stripe_payment_module):
    request = rf.get("/")
    request.shop = get_default_shop()
    request.session = {}
    request.basket = get_basket(request)
    checkout_phase = StripeCheckoutPhase(request=request)
    checkout_phase.module = stripe_payment_module
    assert not checkout_phase.is_valid()  # We can't be valid just yet
    context = checkout_phase.get_context_data()
    assert context["stripe"]
    request.method = "POST"
    token = get_stripe_token(stripe_payment_module)
    request.POST = {
        "stripeToken": token["id"],
        "stripeTokenType": token["type"],
        "stripeTokenEmail": token.get("email"),
    }
    checkout_phase.post(request)
    assert checkout_phase.is_valid()  # We should be valid now
    assert request.session  # And things should've been saved into the session
    checkout_phase.process()  # And this should do things to the basket
    assert request.basket.payment_data.get("stripe")
