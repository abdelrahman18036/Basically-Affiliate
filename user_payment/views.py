from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from Profiles.models import Profile
from user_payment.models import UserPayment
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import logging

# Create your views here.
@login_required(login_url='login')
def product_page(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': settings.PRODUCT_PRICE,
                'quantity': 1,
            }],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )

        return redirect(checkout_session.url, code=303)
    return render(request, 'product_page.html')

def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    profile = Profile.objects.get(user=request.user)
    user_payment = UserPayment.objects.create(
        app_user=profile,
        stripe_session_id=checkout_session_id,
        payment_bool=True,
    )

    profile.payment_sucessful_ref = user_payment
    profile.save()
    
    return render(request, 'payment_successful.html', {'customer': session.customer})



def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, 'payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)