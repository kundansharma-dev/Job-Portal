from django.shortcuts import render,redirect
from .models import  *
from random import randint   #  otp ke liye module import kiya

# Create your views here.

def indexpage(request):
    return render(request,'app/index.html')


def SignupPage(request):
    return render(request,'app/signup.html')

def register(request):
    return render(request,'app/signup.html')

def RegisterUser(request):
    if request.POST['role']=='Candidate':
        
        role=request.POST['role']
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        user= UserMaster.objects.filter(email=email)

        if user:
            message="User already Exist"
            return render(request,'app/signup.html',{'msg':message})
        else:
            if password==cpassword:
                otp=randint(10000,999999)
                newuser=UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                newcand=Candidate.objects.create(user_id=newuser,firstname=fname,lastname=lname)
                return render(request,'app/otpverify.html',{'email':email})
    else:
        print('Company Registration') # yaha mujhe company ka views banana hai 


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

        user = UserMaster.objects.filter(email=email).first()

        if user:
            if user.password == password and user.role == role:
                can = Candidate.objects.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = can.firstname
                request.session['lastname'] = can.lastname
                request.session['email'] = user.email
                return redirect('index')
            else:
                return render(request, 'app/login.html', {'msg': 'Invalid credentials'})
        else:
            return render(request, 'app/login.html', {'msg': 'User does not exist'})

    return render(request, 'app/login.html')
# profile views

def ProfilePage(request,pk):
    user=UserMaster.objects.get(pk=pk)
    can=Candidate.objects.get(user_id=user)
    return render(request,'app/profile.html',{'user':user,'can':can})


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


def logout_user(request):
    request.session.flush()
    return redirect('loginpage')

                




    









