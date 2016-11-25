# This file is part of Shuup Stripe Addon.
#
# Copyright (c) 2012-2016, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms

from shuup.admin.forms import ShuupAdminForm
from shuup.admin.modules.service_providers.wizard_form_defs import (
    ServiceWizardFormDef
)
from shuup.admin.modules.service_providers.wizard_forms import (
    ServiceWizardForm
)

from .models import StripeCheckoutPaymentProcessor


class StripeCheckoutAdminForm(ShuupAdminForm):
    class Meta:
        model = StripeCheckoutPaymentProcessor
        fields = '__all__'
        widgets = {
            'secret_key': forms.PasswordInput(render_value=True),
            'publishable_key': forms.PasswordInput(render_value=True),
        }


class StripeCheckoutWizardForm(ServiceWizardForm):
    class Meta:
        model = StripeCheckoutPaymentProcessor
        fields = ("name", "service_name", "secret_key", "publishable_key")
        widgets = {
            'secret_key': forms.PasswordInput(render_value=True),
            'publishable_key': forms.PasswordInput(render_value=True),
        }

    def __init__(self, **kwargs):
        super(StripeCheckoutWizardForm, self).__init__(**kwargs)
        if not self.provider:
            return
        service = self.get_payment_method()
        if not service:
            return
        self.fields["service_name"].initial = service.name
        self.fields["secret_key"].initial = self.provider.secret_key
        self.fields["publishable_key"].initial = self.provider.publishable_key


class StripeCheckoutWizardFormDef(ServiceWizardFormDef):
    def __init__(self):
        super(StripeCheckoutWizardFormDef, self).__init__(
            name="stripe",
            form_class=StripeCheckoutWizardForm,
            template_name="shuup/stripe/wizard_form.jinja"
        )
