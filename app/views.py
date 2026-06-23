from django.shortcuts import render,redirect
from .models import  *
from random import randint   #  otp ke liye module import kiya

# Create your views here.

def indexpage(request):
    return render(request,'app/index.html')
def CompanyIndexPage(request):
    return render(request,'app/company-index.html')


def SignupPage(request):
    return render(request,'app/signup.html')

def register(request):
    return render(request,'app/signup.html')

def RegisterUser(request):

    role = request.POST.get('role')
    fname = request.POST.get('firstname')
    lname = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    cpassword = request.POST.get('cpassword')

    user = UserMaster.objects.filter(email=email).first()

    if user:
        return render(request,'app/signup.html',{
            'msg':'User already exists'
        })

    if password != cpassword:
        return render(request,'app/signup.html',{
            'msg':'Password and Confirm Password do not match'
        })

    otp = randint(100000,999999)

    newuser = UserMaster.objects.create(
        role=role,
        email=email,
        password=password,
        otp=otp
    )

    if role == "Candidate":

        Candidate.objects.create(
            user_id=newuser,
            firstname=fname,
            lastname=lname
        )

    elif role == "Company":

        Company.objects.create(
            user_id=newuser,
            company_name=fname   # temporary
        )

    else:
        return render(request,'app/signup.html',{
            'msg':'Invalid Role'
        })

    return render(request,'app/otpverify.html',{
        'email':email
    })

def OTPPage(request):
    return render(request,'app/otpverify.html')


def otpverify(request):
    email=request.POST['email']
    otp=int(request.POST['otp'])

    user=UserMaster.objects.get(email=email)


    if user:
        if user.otp==otp:
            message='Otp verify successfully'
            return render(request,'app/login.html',{'msg':message})
        else:
            message='Otp is incorrect'
            return render(request,'app/otpverify.html',{'msg':message})
    else:
        return render(request,'app/signup.html')



def LoginPage(request):
    return render(request,'app/login.html')

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

            # Candidate Login
            if role == "Candidate":
                can = Candidate.objects.get(user_id=user)

                request.session['firstname'] = can.firstname
                request.session['lastname'] = can.lastname

                return redirect('index')

            # Company Login
            elif role == "Company":
                com = Company.objects.get(user_id=user)

                request.session['company_name'] = com.company_name

                return redirect('company_index')

        else:
            return render(
                request,
                'app/login.html',
                {'msg': 'Invalid Credentials'}
            )

    return render(request, 'app/login.html')
# profile views

def ProfilePage(request,pk):
    user=UserMaster.objects.get(pk=pk)
    can=Candidate.objects.get(user_id=user)
    return render(request,'app/profile.html',{'user':user,'can':can})

def CompanyProfilePage(request, pk):
    user = UserMaster.objects.get(pk=pk)
    company = Company.objects.get(user_id=user)

    return render(
        request,
        'app/company-profile.html',
        {'user': user, 'company': company}
    )


def UpdateProfile(request, pk):
    user = UserMaster.objects.get(pk=pk)

    if request.method == "POST":

        if user.role == 'Candidate':
            can = Candidate.objects.get(user_id=user)

            can.contact = request.POST['contact']
            can.city = request.POST['city']
            can.address = request.POST['address']
            can.dob = request.POST['dob']
            can.gender = request.POST['gender']
            can.country = request.POST['country']
            can.website = request.POST['website']
            can.job_type = request.POST['job_type']
            can.job_catagry = request.POST['job_catagry']
            can.job_description = request.POST['job_description']
            can.min_salary = request.POST['min_salary']
            can.max_salary = request.POST['max_salary']

            if request.FILES.get('profile_pic'):
                can.profile_pic = request.FILES['profile_pic']

            can.save()
            return redirect(f'/profile/{pk}')

    return redirect(f'/profile/{pk}')

def UpdateCompanyProfile(request, pk):

    user = UserMaster.objects.get(pk=pk)
    company = Company.objects.get(user_id=user)

    if request.method == "POST":

        company.company_name = request.POST['company_name']
        company.company_address = request.POST['company_address']
        company.company_city = request.POST['company_city']
        company.company_country = request.POST['company_country']

        company.company_contact = request.POST['company_contact']
        company.company_website = request.POST['company_website']
        company.company_description = request.POST['company_description']

        if request.FILES.get('company_logo'):
            company.company_logo = request.FILES['company_logo']

        company.save()

        return redirect(f'/company-profile/{pk}/')

    return redirect(f'/company-profile/{pk}/')


def logout_user(request):
    request.session.flush()
    return redirect('loginpage')

                




    









