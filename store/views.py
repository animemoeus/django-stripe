from django.shortcuts import get_object_or_404, redirect, render

from .models import PaymentLink


def update_session(request, session_id):
    payment_link = get_object_or_404(PaymentLink, stripe_session_id=session_id)
    payment_link.update_payment_status()

    return redirect("/")
