from django.shortcuts import render

from django.urls import reverse

from paypal.standard.forms import PayPalPaymentsForm

from django.conf import settings

import uuid
import time

from donation.models import Donation

import stripe


def my_donation(request):
    # get the current host of the requested website
    host = request.get_host()

    # get item from donation model
    donation = Donation.objects.get(id=1)

    # paypal dict
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": donation.amount,
        "item_name": donation.title,
        "no_shipping": "2",
        "invoice": str(uuid.uuid4()),
        "currency_code": "CZK",
        "notify_url": f"http://{host}{reverse('paypal-ipn')}",
        "return_url": f"http://{host}{reverse('payment-success')}",
        "cancel_return": f"http://{host}{reverse('payment-failed')}",
    }

    paypal_form = PayPalPaymentsForm(initial=paypal_dict)

    # stripe functionality
    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        line_items=[{
            'price': "price_1OW2VlI53xigQc5rp4bARloC",
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment-success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('payment-failed')),
    )

    return render(request, "donation/my-donation.html", {"paypal_form": paypal_form, 'session_id': session.id,
                                                         'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


def payment_success(request):
    # time.sleep(10)
    return render(request, "donation/payment-success.html")


def payment_failed(request):
    return render(request, "donation/payment-failed.html")
