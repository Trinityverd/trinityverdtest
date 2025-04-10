from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Validate that fields are not empty
        if not username or not password:
            messages.error(request, "Both fields are required.")
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect("login")

