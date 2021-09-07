from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm

def home_page(request):
	# print(request.session.get("first_name", "Unknown"))
	context = {
		"title": "Salam!",
		"content": "Welcome to Updeal, Crazy deals round the clock!",
		"premium_content": "premium! just for you, Yeahhhh!"
	}
	return render(request, "home_page.html", context)



def about_page(request):
	context = {
		"title": "About Updeal",
		"content": "About Updeal!"
	}
	return render(request, "home_page.html", context)


def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		"title": "So, what's up!",
		"content": "Contact Page",
		"form": contact_form
	}
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
		if request.is_ajax():
			return JsonResponse({"message": "Thanks! your message is submitted, we'll be in touch with you shortly. Happy Updealing"})

	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')
	# if request.method == "POST":
	# 	print(request.POST)
	# 	print(request.POST.get("fullname"))
	# 	print(request.POST.get("email"))
	# 	print(request.POST.get("content"))
	return render(request, "contact/view.html", context)