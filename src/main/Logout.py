from django.http import HttpResponseRedirect
from django.shortcuts import render


def logout(request):
    print("Logout Called...")
    request.session['authentication'] = False
    return HttpResponseRedirect('/login')
    # return render(request, "Login/index.html")
