from django.shortcuts import render


def logout(request):
    print("Logout Called...")
    request.session['authentication'] = False
    return render(request, "Login/index.html")
