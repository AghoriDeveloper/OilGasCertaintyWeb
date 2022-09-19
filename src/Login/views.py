import sys

from django.http import HttpResponseRedirect

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

                request.session['user_id'] = data[0][0]
                request.session['user_name'] = data[0][1]
                request.session['user_email'] = data[0][2]
                request.session['obja'] = data[0][4]
                request.session['objb'] = data[0][5]
                request.session['objc'] = data[0][6]
                request.session['objabc'] = data[0][7]

                if request.session['obja'] == 1:
                    object = '/obj-a'
                elif request.session['objb'] == 1:
                    object = '/obj-b'
                elif request.session['objc'] == 1:
                    object = '/obj-c'
                elif request.session['objabc'] == 1:
                    object = '/obj-abc'

                if data != ():
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        request.session['authentication'] = True
                        return HttpResponseRedirect(object)
                    else:
                        userModel = User.objects.create_user(username, username, password)
                        userModel.save()
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            request.session['authentication'] = True
                            return HttpResponseRedirect(object)
                        else:
                            print("login failed...")
                else:
                    return render(request, "Login/index.html", {"warning": "Wrong Credentials !!!"})

            else:
                return render(request, "Login/index.html", {"warning": "Email doesn't exists..."})

    # return render(request, "Login/index.html", {'form': objc})
    return render(request, "Login/index.html")
