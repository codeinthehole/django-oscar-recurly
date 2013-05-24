====================================
Recurly integration for django-oscar
====================================

This package provides integration with the payment gateway, Recurly using their API and push notifications. It is designed to work seamlessly with the e-commerce framework `django-oscar`.

* `Recurly API`: https://docs.recurly.com/api
* `Recurly Push Notifications`: https://docs.recurly.com/api/push-notifications
* `django-oscar`: https://github.com/tangentlabs/django-oscar

Installation
------------

From PyPi::

    pip install django-oscar-recurly

or from Github::

    pip install git+git://github.com/mynameisgabe/django-oscar-recurly.git#egg=django-oscar-recurly

Add ``'recurly'`` to ``INSTALLED_APPS`` and run::

    ./manage.py migrate recurly

to create the appropriate database tables.

Configuration
-------------

Edit your ``settings.py`` to set the following settings::

    RECURLY_SUBDOMAIN = 'your-subdomain'
    RECURLY_API_KEY = 'abcdef01234567890abcdef01234567890'
    RECURLY_PRIVATE_KEY = '01234567890abcdef01234567890abcdef'
    RECURLY_DEFAULT_CURRENCY = 'USD'

Integration into checkout
-------------------------

You'll need to use a subclass of ``oscar.apps.checkout.views.PaymentDetailsView`` within your own
checkout views.  See `oscar's documentation`_ on how to create a local version of the checkout app.

.. _`oscar's documentation`: http://django-oscar.readthedocs.org/en/latest/index.html

Override the ``handle_payment`` method (which is blank by default) and add your integration code.  An example
integration might look like::

    # myshop.checkout.views
    from django.conf import settings

    from oscar.apps.checkout.views import PaymentDetailsView as OscarPaymentDetailsView
    from oscar.apps.payment.forms import BankcardForm
    from recurly.facade import Facade
    from recurly import RECURLY

    ...

    class PaymentDetailsView(OscarPaymentDetailsView):

        def get_context_data(self, **kwargs):
            ...
            ctx['bankcard_form'] = BankcardForm()
            ...
            return ctx

        def post(self, request, *args, **kwargs):
            """
            This method is designed to be overridden by subclasses which will
            validate the forms from the payment details page.  If the forms are valid
            then the method can call submit()
            """
            # Check bankcard form is valid
            bankcard_form = BankcardForm(request.POST)
            if not bankcard_form.is_valid():
                ctx = self.get_context_data(**kwargs)
                ctx['bankcard_form'] = bankcard_form
                return self.render_to_response(ctx)

            bankcard = bankcard_form.get_bankcard_obj()

            # Call oscar's submit method, passing through the bankcard object so it gets
            # passed to the 'handle_payment' method
            return self.submit(request.basket, payment_kwargs={'bankcard': bankcard})

        def handle_payment(self, order_number, total, **kwargs):
            # Make request to Recurly - if there any problems (eg bankcard
            # not valid / request refused by bank) then an exception would be
            # raised and handled) within oscar's PaymentDetails view.
            bankcard = kwargs['bankcard']
            response_dict = Facade().purchase(order_number, total, None, bankcard)

            source_type, _ = SourceType.objects.get_or_create(name=RECURLY)
            source = Source(source_type=source_type,
                            currency=settings.RECURLY_DEFAULT_CURRENCY,
                            amount_allocated=total,
                            amount_debited=total,
                            reference=response_dict['partner_reference'])

            self.add_payment_source(source)

            # Also record payment event
            self.add_payment_event(PURCHASE, total)

Oscar's view will handle the various exceptions that can get raised.

Package structure
=================

There are two key components:

Gateway
-------

The class ``recurly.gateway.Gateway`` provides fine-grained access to the Recurly API, which involve constructing XML requests and decoding XML responses.  All calls return a ``recurly.gateway.Response`` instance which provides dictionary-like access to the attributes of the response.

Example calls::

    # Authorise a transaction.
    # The funds are not transferred from the cardholder account.
    response = gateway.authorise(card_holder='John Smith',
                                 card_number='4500230021616301',
                                 cvc2='123',
                                 amount=50.23)

    # Completes (settles) a pre-approved Auth Transaction.
    response = gateway.complete(amount=50.23,
                                dps_txn_ref='0000000809b61753')


    # Purchase on a new card - funds are transferred immediately
    response = gateway.purchase(card_holder='Frankie',
                                card_number=CARD_VISA,
                                card_expiry='1015',
                                cvc2='123',
                                merchant_ref='100001_PURCHASE_1_2008',
                                enable_add_bill_card=1,
                                amount=29.95)

    # Purchase on a previously used card
    response = gateway.purchase(amount=29.95,
                                billing_id='0000080023748351')


    # Refund a transaction - funds are transferred immediately
    response = gateway.refund(dps_txn_ref='0000000809b61753',
                              merchant_ref='abc123',
                              amount=50.23)

Facade
------

The class ``recurly.facade.Facade`` wraps the above gateway object and provides a less granular API, as well as saving instances of ``recurly.models.OrderTransaction`` to provide an audit trail for Recurly activity.


Settings
========

* ``RECURLY_SUBDOMAIN`` - Subdomain for Recurly Account

* ``RECURLY_API_KEY`` - API Key

* ``RECURLY_PRIVATE_KEY`` - Private Key

* ``RECURLY_DEFAULT_CURRENCY`` - Currency to use for transactions


Contributing
============

To work on ``django-oscar-recurly``, clone the repo, set up a virtualenv and install in develop mode::

    python setup.py develop

then install the testing dependencies::

    pip install -r requirements.txt

The test suite can then be run using::

    ./runtests.py

Magic card numbers are available on the Recurly site:
https://docs.recurly.com/payment-gateways/test

Sample VISA vard:

    4111111111111111
    
[![Build Status](https://travis-ci.org/mynameisgabe/django-oscar-recurly.png?branch=master)](https://travis-ci.org/mynameisgabe/django-oscar-recurly)