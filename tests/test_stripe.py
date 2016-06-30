# -*- coding: utf-8 -*-
# This file is part of Shuup Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.utils.timezone import now
import os

import pytest
from shuup.front.basket import get_basket
from shuup.utils.excs import Problem
from shuup.testing.factories import (
    get_default_product,
    get_default_supplier,
    get_default_tax_class,
    create_order_with_product,
    get_default_shop)
from shuup.utils.http import retry_request

from shuup_stripe.checkout_phase import StripeCheckoutPhase
from shuup_stripe.models import StripeCheckoutPaymentProcessor


@pytest.fixture
def stripe_payment_processor():
    sk = os.environ.get("STRIPE_SECRET_KEY")
    if not sk:
        pytest.skip("Can't test Stripe without STRIPE_SECRET_KEY envvar")
    if "test" not in sk:
        pytest.skip("STRIPE_SECRET_KEY is not a test key")

    return StripeCheckoutPaymentProcessor.objects.create(
        secret_key=sk, publishable_key="x")


def _create_order_for_stripe(stripe_payment_processor):
    product = get_default_product()
    supplier = get_default_supplier()
    order = create_order_with_product(
        product=product, supplier=supplier, quantity=1,
        taxless_base_unit_price=100, tax_rate=0
    )
    payment_method = stripe_payment_processor.create_service(
        None, shop=order.shop, tax_class=get_default_tax_class(), enabled=True)
    order.payment_method = payment_method
    order.cache_prices()
    assert order.taxless_total_price.value > 0
    if not order.payment_data:
        order.payment_data = {}
    order.save()
    return order


def get_stripe_token(stripe_payment_processor):
    return retry_request(
        method="post",
        url="https://api.stripe.com/v1/tokens",
        auth=(stripe_payment_processor.secret_key, "x"),
        data={
            "card[number]": "4242424242424242",
            "card[exp_month]": 12,
            "card[exp_year]": now().date().year + 1,
            "card[cvc]": 666,
        }
    ).json()


##############################################################################

@pytest.mark.django_db
def test_stripe_basics(rf, stripe_payment_processor):
    """
    :type rf: RequestFactory
    :type stripe_payment_module: StripeCheckoutModule
    """
    order = _create_order_for_stripe(stripe_payment_processor)
    token = get_stripe_token(stripe_payment_processor)
    token_id = token["id"]
    order.payment_data["stripe"] = {"token": token_id}
    order.save()
    service = order.payment_method
    stripe_payment_processor.process_payment_return_request(
        service, order, rf.post("/"))
    assert order.is_paid()
    assert order.payments.first().payment_identifier.startswith("Stripe-")


@pytest.mark.django_db
def test_stripe_bogus_data_fails(rf, stripe_payment_processor):
    order = _create_order_for_stripe(stripe_payment_processor)
    order.payment_data["stripe"] = {"token": "ugubugudugu"}
    order.save()
    with pytest.raises(Problem):
        stripe_payment_processor.process_payment_return_request(
            order.payment_method,
            order,
            rf.post("/")
        )


@pytest.mark.django_db
def test_stripe_checkout_phase(rf, stripe_payment_processor):
    request = rf.get("/")
    request.shop = get_default_shop()
    request.session = {}
    request.basket = get_basket(request)
    service = stripe_payment_processor.create_service(
        None, shop=request.shop, tax_class=get_default_tax_class(),
        enabled=True)
    checkout_phase = StripeCheckoutPhase(
        request=request, service=service)
    assert not checkout_phase.is_valid()  # We can't be valid just yet
    context = checkout_phase.get_context_data()
    assert context["stripe"]
    request.method = "POST"
    token = get_stripe_token(stripe_payment_processor)
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


@pytest.mark.django_db
def test_stripe_checkout_phase_with_misconfigured_module(rf):
    stripe_payment_prossor = (
        StripeCheckoutPaymentProcessor.objects.create())
    request = rf.get("/")
    request.shop = get_default_shop()
    request.session = {}
    request.basket = get_basket(request)
    service = stripe_payment_prossor.create_service(
        None, shop=request.shop, tax_class=get_default_tax_class(),
        enabled=True)
    checkout_phase = StripeCheckoutPhase(
        request=request, service=service)
    with pytest.raises(Problem):
        checkout_phase.get_context_data()
