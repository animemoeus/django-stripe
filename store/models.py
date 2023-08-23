import stripe
from django.conf import settings
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField(help_text="The price of the product (USD)")

    stripe_product_id = models.CharField(
        max_length=255, default="", blank=True, null=True
    )
    stripe_price_id = models.CharField(
        max_length=255, default="", blank=True, null=True
    )
    stripe_session_id = models.CharField(
        max_length=255, default="", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.create_or_update_stripe_product()
        self.create_or_update_stripe_product_price()

        super(Product, self).save(*args, **kwargs)

    def create_or_update_stripe_product(self):
        """
        Try to create or update the product based on `stripe_product_id`
        """
        try:
            result = stripe.Product.retrieve(self.stripe_product_id)
            if result:
                stripe.Product.modify(
                    self.stripe_product_id, name=self.name, description=self.description
                )
        except stripe.error.InvalidRequestError:  # create
            result = stripe.Product.create(name=self.name)
            self.stripe_product_id = result["id"]

    def create_or_update_stripe_product_price(self):
        try:
            result = stripe.Price.retrieve(
                self.stripe_price_id,
            )

            # currently stripe API does not support for deleting the price
            # so we need to check if current product has `stripe_price_id`
            # and if the price for the current `stripe_price_id` is changed, then we deactivate the old price and create a new one
            # https://github.com/stripe/stripe-python/issues/658
            if (
                result["unit_amount"] != self.price * 100
                or self.stripe_product_id != result["product"]
            ):
                stripe.Price.modify(self.stripe_price_id, active=False)
                result = stripe.Price.create(
                    unit_amount=self.price * 100,
                    currency="usd",
                    product=self.stripe_product_id,
                )
            self.stripe_price_id = result["id"]
        except stripe.error.InvalidRequestError:
            result = stripe.Price.create(
                unit_amount=self.price * 100,
                currency="usd",
                product=self.stripe_product_id,
            )
            self.stripe_price_id = result["id"]

    def create_checkout_session(self):
        result = stripe.checkout.Session.create(
            success_url="https://animemoe.us",
            line_items=[
                {
                    "price": self.stripe_price_id,
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        self.stripe_session_id = result["id"]

    @property
    def checkout_url(self):
        result = stripe.checkout.Session.retrieve(
            self.stripe_session_id,
        )

        return result["url"] if result else None
