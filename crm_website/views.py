from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . forms import SignUpForm,AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in!")
            return redirect('home')
        else:
            messages.success(request,"Please enter correct credentials....")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out....")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'register.html',{'form':form})

def customer_record(request,id):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(pk=id)
        return render(request,"record.html",{"record":customer_record})
    else:
        messages.success(request,"To access record you must have to Logged In!")
        return redirect('home')

def delete_record(request,id):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=id)
        record.delete()
        messages.success(request,"Record deleted successfully")
        return redirect("home")
    else:
        messages.success(request,"To delete record you must have to Logged In!")
        return redirect("home")

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = form.save()
                messages.success(request,"Record addedd.....")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"To add record you must have to Logged In!")
        return redirect('home')

def update_record(request,id):
    if request.user.is_authenticated:
        current_record = Record.objects.get(pk=id)
        form = AddRecordForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been updated....")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"To update record you must have to Log In!")
        return redirect('home')