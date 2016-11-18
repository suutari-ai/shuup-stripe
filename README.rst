.. image:: https://travis-ci.org/shuup/shuup-stripe.svg?branch=master
    :target: https://travis-ci.org/shuup/shuup-stripe
.. image:: https://coveralls.io/repos/github/shuup/shuup-stripe/badge.svg?branch=master
    :target: https://coveralls.io/github/shuup/shuup-stripe?branch=master

Shuup Stripe Addon
==================

This package implements `Stripe Checkout <https://stripe.com/checkout>`__
for the `Shuup <https://shuup.com/>`__ platform.

Copyright
---------

Copyright (c) 2012-2016 by Shoop Commerce Ltd. <contact@shuup.com>

Shuup is International Registered Trademark & Property of Shoop Commerce Ltd.,
Business ID: FI24815722, Business Address: Aurakatu 12 B, 20100 Turku,
Finland.

License
-------

Shuup Stripe Addon is published under the GNU Affero General Public License,
version 3 (AGPLv3). See the LICENSE file.

Running tests
-------------

Tests are run with `py.test <http://pytest.org/>`__.  If you already have
a virtualenv where you are able to run Shuup's tests, you should be able
to run these in the same virtualenv.  A stub `package.json` exists with
a properly configured `test` script, so all you need to do is::

    npm test
