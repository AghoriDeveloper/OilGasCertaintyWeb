import sys

import mysql.connector.errors
from django.http import HttpResponseRedirect

sys.path.append("..")

from django.shortcuts import render
from .forms import RegisterForm
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

    return render(request, "Register/index.html")
