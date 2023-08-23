from django.shortcuts import render

from store.models import Product


def index(request):
    context = {}

    products = Product.objects.all().order_by("-id")
    if products:
        context["products"] = products

    return render(request, "index.html", context)
