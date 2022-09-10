import sys
sys.path.append("..")

from django.shortcuts import render
from .forms import LoginForm
# from .processing import setObjecCValues
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import mysql.connector as sql


def index(request):
    global warning
    login = LoginForm()

    if request.method == 'POST':
        warning = False
        login = LoginForm(request.POST)
        if login.is_valid():
            username = request.POST['email']
            password = request.POST['password']

            m = sql.connect(host="localhost", user="root", passwd="", database="OilGasCertainty")
            # m = sql.connect(host="localhost", user="oilgascertainty_user", passwd="OGCUser@321", database="oilgascertainty")
            cursor = m.cursor()
            sql_query = "SELECT * FROM users WHERE email='{}'".format(username)
            cursor.execute(sql_query)
            data = tuple(cursor.fetchall())

            if data != ():
                m = sql.connect(host="localhost", user="root", passwd="", database="OilGasCertainty")
                # m = sql.connect(host="localhost", user="oilgascertainty_user", passwd="OGCUser@321", database="oilgascertainty")
                cursor = m.cursor()
                sql_query = "SELECT * FROM users WHERE email='{}' AND password ='{}'".format(username, password)
                cursor.execute(sql_query)
                data = tuple(cursor.fetchall())

                if data != ():
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        request.session['authentication'] = True
                        print("login successful...")
                        return render(request, "ObjectA/index.html")
                    else:
                        userModel = User.objects.create_user(username, username, password)
                        userModel.save()
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            request.session['authentication'] = True
                            print("login successful...")
                            return render(request, "ObjectA/index.html")
                        else:
                            print("login failed...")
                else:
                    return render(request, "Login/index.html", {"warning": "Wrong Credentials !!!"})

            else:
                return render(request, "Login/index.html", {"warning": "Email doesn't exists..."})

    # return render(request, "Login/index.html", {'form': objc})
    return render(request, "Login/index.html")
