from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from accounts.models import Token
from django.core.urlresolvers import reverse
from django.contrib import auth, messages

def send_login_email(request):
	email = request.POST['email']
	token = Token.objects.create(email=email)
	url = request.build_absolute_uri(
		reverse('login') + '?token={uid}'.format(uid=str(token.uid)))
	message_body = "Use this link to login:\n\n{url}".format(url=url)
	
	send_mail(
		'Your login link for To-do',
		message_body,
		'noreply@todo',
		[email],)

	messages.success(request, "Check your email, we have sent you a link you can use to login")
	return redirect('/')

def login(request):
	user = auth.authenticate(uid=request.GET.get('token'))
	if user:
		auth.login(request, user)
	return redirect('/')