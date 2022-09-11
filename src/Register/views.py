import sys

import mysql.connector.errors
from django.http import HttpResponseRedirect

sys.path.append("..")

from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import mysql.connector as sql


def index(request):
    if request.method == 'POST':
        warning = False
        register = RegisterForm(request.POST)
        if register.is_valid():
            name = request.POST['name']
            username = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                m = sql.connect(host="localhost", user="root", passwd="", database="OilGasCertainty")
                # m = sql.connect(host="localhost", user="oilgascertainty_user", passwd="OGCUser@321", database="oilgascertainty")
                cursor = m.cursor()
                sql_query = "INSERT INTO users (name, email, password) VALUES ('{}', '{}', '{}')".format(name, username, password)
                print(sql_query)
                try:
                    cursor.execute(sql_query)
                except mysql.connector.errors.IntegrityError:
                    return render(request, "Register/index.html", {"warning": "This email already exists..."})
                m.commit()
                return HttpResponseRedirect('/login')
            else:
                return render(request, "Register/index.html", {"warning": "Both passwords must be same."})

            # m = sql.connect(host="localhost", user="root", passwd="", database="OilGasCertainty")
            # # m = sql.connect(host="localhost", user="oilgascertainty_user", passwd="OGCUser@321", database="oilgascertainty")
            # cursor = m.cursor()
            # sql_query = "SELECT * FROM users WHERE email='{}'".format(username)
            # cursor.execute(sql_query)
            # data = tuple(cursor.fetchall())
            #
            # if data != ():
            #     m = sql.connect(host="localhost", user="root", passwd="", database="OilGasCertainty")
            #     # m = sql.connect(host="localhost", user="oilgascertainty_user", passwd="OGCUser@321", database="oilgascertainty")
            #     cursor = m.cursor()
            #     sql_query = "SELECT * FROM users WHERE email='{}' AND password ='{}'".format(username, password)
            #     cursor.execute(sql_query)
            #     data = tuple(cursor.fetchall())
            #
            #     if data != ():
            #         user = authenticate(request, username=username, password=password)
            #         if user is not None:
            #             request.session['authentication'] = True
            #             print("login successful...")
            #             return render(request, "ObjectA/index.html")
            #         else:
            #             userModel = User.objects.create_user(username, username, password)
            #             userModel.save()
            #             user = authenticate(request, username=username, password=password)
            #             if user is not None:
            #                 request.session['authentication'] = True
            #                 print("login successful...")
            #                 return render(request, "ObjectA/index.html")
            #             else:
            #                 print("login failed...")
            #     else:
            #         return render(request, "Login/index.html", {"warning": "Wrong Credentials !!!"})
            #
            # else:
            #     return render(request, "Login/index.html", {"warning": "Email doesn't exists..."})

    return render(request, "Register/index.html")
