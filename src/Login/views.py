import sys
sys.path.append("..")

from django.shortcuts import render
from .forms import LoginForm
# from .processing import setObjecCValues
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def index(request):
    login = LoginForm()

    if request.method == 'POST':
        login = LoginForm(request.POST)
        if login.is_valid():
            print(login['email'].value(), login['password'].value())
            # response = setObjecCValues(objc['product'].value(), objc['threshold'].value(), objc['bc_mmscfg'].value(), objc['gor'].value(), objc['curveType'].value(), import_file_path, objc['fixedCost'].value(), objc['indProdCost'].value(), objc['oilProdCost'].value(), objc['gasProdCost'].value(), objc['costBelowPerc'].value(), objc['indProdSD'].value())
            # return response
            # objc.save()

            username = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login
                request.session['authentication'] = True
                print("login successful...")
                return render(request, "ObjectA/index.html")
            else:
                userModel = User.objects.create_user(username, username, password)
                userModel.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login
                    request.session['authentication'] = True
                    print("login successful...")
                    return render(request, "ObjectA/index.html")
                else:
                    print("login failed...")

    # return render(request, "Login/index.html", {'form': objc})
    return render(request, "Login/index.html")
