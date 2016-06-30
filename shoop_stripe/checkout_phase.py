# -*- coding: utf-8 -*-
# This file is part of Shoop Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.views.generic.edit import FormView
from shoop.front.checkout import (
    BasicServiceCheckoutPhaseProvider, CheckoutPhaseViewMixin
)
from shoop.utils.excs import Problem

from .models import StripeCheckoutPaymentProcessor
from .utils import get_amount_info


class StripeTokenForm(forms.Form):
    # We're using camel case here only because that's what Stripe does
    stripeToken = forms.CharField(widget=forms.HiddenInput, required=True)
    stripeTokenType = forms.CharField(widget=forms.HiddenInput, required=False)
    stripeEmail = forms.CharField(widget=forms.HiddenInput, required=False)


class StripeCheckoutPhase(CheckoutPhaseViewMixin, FormView):
    service = None  # Injected by the method phase
    identifier = "stripe"
    title = "Stripe"
    template_name = "shoop/stripe/checkout_phase.jinja"
    form_class = StripeTokenForm

    def get_stripe_context(self):
        payment_processor = self.service.payment_processor
        publishable_key = payment_processor.publishable_key
        secret_key = payment_processor.secret_key
        if not (publishable_key and secret_key):
            raise Problem(
                _("Please configure Stripe keys for payment processor %s.") %
                payment_processor)

        config = {
            "publishable_key": publishable_key,
            "name": force_text(self.request.shop),
            "description": force_text(_("Purchase")),
        }
        config.update(get_amount_info(self.request.basket.taxful_total_price))
        return config

    def get_context_data(self, **kwargs):
        context = super(StripeCheckoutPhase, self).get_context_data(**kwargs)
        context["stripe"] = self.get_stripe_context()
        return context

    def is_valid(self):
        return "token" in self.storage.get("stripe", {})

    def form_valid(self, form):
        self.storage["stripe"] = {
            "token": form.cleaned_data.get("stripeToken"),
            "token_type": form.cleaned_data.get("stripeTokenType"),
            "email": form.cleaned_data.get("stripeEmail"),
        }
        return super(StripeCheckoutPhase, self).form_valid(form)

    def process(self):
        self.request.basket.payment_data["stripe"] = self.storage["stripe"]


class StripeCheckoutPhaseProvider(BasicServiceCheckoutPhaseProvider):
    phase_class = StripeCheckoutPhase
    service_provider_class = StripeCheckoutPaymentProcessor
