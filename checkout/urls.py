"""checkout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app1.views import CreateCheckoutSessionView, ProductLandingPageView, SuccessView, CancelView, StripeIntentView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app1.urls')),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='submit'),
    path('', ProductLandingPageView.as_view(), name='landing-page'),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-payment-intent'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    # path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]
