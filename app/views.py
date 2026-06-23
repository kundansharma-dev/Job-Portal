from django.shortcuts import render, redirect
from .models import *

def LoginUser(request):
    if request.method == "POST":

        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = UserMaster.objects.filter(
            email=email,
            password=password,
            role=role
        ).first()

        if user:

            request.session['id'] = user.id
            request.session['role'] = user.role
            request.session['email'] = user.email

            # ---------------- SAFE CANDIDATE LOGIN ----------------
            if role == "Candidate":
                can = Candidate.objects.filter(user_id=user).first()

                if can:
                    request.session['firstname'] = can.firstname
                    request.session['lastname'] = can.lastname

                return redirect('index')

            # ---------------- SAFE COMPANY LOGIN ----------------
            elif role == "Company":
                com = Company.objects.filter(user_id=user).first()

                if com:
                    request.session['company_name'] = com.company_name

                return redirect('company_index')

        return render(request, 'app/login.html', {
            'msg': 'Invalid Credentials'
        })

    return render(request, 'app/login.html')