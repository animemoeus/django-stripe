from django.shortcuts import render

from store.models import PaymentLink, Product


def index(request):
    context = {}

    products = Product.objects.all().order_by("-id")
    if products:
        context["products"] = products

    payment_links = PaymentLink.objects.all().order_by("-id")
    if payment_links:
        context["payment_links"] = payment_links

    return render(request, "index.html", context)
