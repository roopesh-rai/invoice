from django.shortcuts import render, redirect
import stripe
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views import View
from django.http import HttpResponse
from django.core.mail import send_mail
from .models import Product
from django.http import JsonResponse
# Create your views here

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"

class CancelView(TemplateView):
    template_name = "cancel.html"

class ProductLandingPageView(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="Test product")
        context = super(ProductLandingPageView, self).get_context_data(**kwargs)
        context.update({
            "product":product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'price': '{{product.price}}',
                    'price': product.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return redirect(checkout_session.url, code=303)

endpoint_secret = 'whsec_a02f2df803ffa596f42eed01d433d199d66144766f636cd3bf1fe207a14448b4'
@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  print(sig_header)
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  if event['type'] == 'checkout.session.completed':
      session = event['data']['object']

      customer_email = session["customer_details"]["email"]
      product_id = session["metadata"]["product_id"]
      # Fulfill the purchase...
      # fulfill_order(session)

      # product = Product.objects.get(id=product_id)
      product = Product.objects.get(title="Realme C21Y 32 GB")

      send_mail(
          subject="Here is your product",
          message="Thanks for your purchase. The URL is {product.url}",
          recipient_list=[customer_email],
          from_email="roopesh.rai@plutustec.com",
      )

  # Passed signature verification
  return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(title="Realme C21Y 32 GB")
            intent = stripe.PaymentIntent.create(
                amount=product.discounted_price,
                currency='INR',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})