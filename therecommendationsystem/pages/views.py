from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm,ContactUsForm
from django.db.models import Q
from django.contrib import messages
from .models import Contactus,Places,Myrating
import requests
from django.contrib.auth.decorators import login_required
from ast import literal_eval as make_tuple
import json
import csv


# Create your views here.
#--Home view-->
def home(request):
    context = Places.objects.all()
    query = request.GET.get('q')
    if query:
        contexts = Places.objects.filter(Q(name__icontains=query)).distinct()
        return render(request, 'home.html', {'context': contexts})

    return render(request,"home.html",{'context': context})


#--Rating view-->
def rating(request, place_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    places = get_object_or_404(Places, id=place_id)
    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObjectss = Myrating()
        ratingObjectss.user = request.user
        ratingObjectss.places = places
        ratingObjectss.rating = rate
        ratingObjectss.save()

        return redirect("home")
    return render(request, 'rating.html', {'place': places})

#--About view-->
def about(request):
    return render(request,"aboutus.html",{})

#--Contact view-->
def contact(request):
    my_con_form = ContactUsForm(request.GET)
    if request.method=="POST":
        my_con_form = ContactUsForm(request.POST)
        if my_con_form.is_valid():
            Contactus.objects.create(**my_con_form.cleaned_data)
            return redirect("contact")


    context = {"form":my_con_form}
    return render(request,"contactus.html",context)

#--Register view-->
def register(request):
    form_pre = UserForm()
    if request.method == 'POST':
        form_pre = UserForm(request.POST)
        if form_pre.is_valid():
            form_pre.save()
            messages.success(request, 'Account created successfully..')
            return redirect('login')
    context = {'form': form_pre}
    return render(request,"register.html",context)

#--Login view-->
def loginuser(request):
    if request.method == 'POST':

        username_entered = request.POST.get('username')
        password_entered = request.POST.get('password')

        user = authenticate(request,username = username_entered, password = password_entered)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"username or password is incorrect...")
    context = {}
    return render(request,"login.html",context)

#--Logout view-->
def logoutuser(request):
    logout(request)
    return redirect('home')

##--Recommend view-->
@login_required(login_url='login')
def recommend(request):
    get_user_id = request.user.id
    url = "http://127.0.0.1:5000/recommend"
    payload = {'user_id':get_user_id}
    headers = {
        'content-type': "multipart/form-data",
        'cache-control': "no-cache",

    }

    responses = requests.request("POST",url,data=payload)
    # import pdb;pdb.set_trace()
    response = json.loads(responses.text)
    respnses_tuple = make_tuple(response)
    context = list()

    for user_id in respnses_tuple:
        try:
            recommended = Places.objects.get(id=user_id)
            context.append(recommended)
        except:
            pass

    return render(request,"recommend.html",{'context': context})
#new-->
@login_required(login_url='login')
def dashboard(request):
    print('Dashboard')
    final_list = []
    csv_fp = open('restaurant.csv', 'r')

    reader = csv.DictReader(csv_fp)
    headers = [col for col in reader.fieldnames if col != 'Unnamed: 0']
    for row in reader:
        data_list = []
        data_list.append(row['Restaurant Name'])
        data_list.append(row['Address'])
        data_list.append(row['Online Order'])
        data_list.append(row['Book Table'])
        data_list.append(row['Rate'])
        data_list.append(row['Phone'])
        data_list.append(row['Restaurant Type'])
        data_list.append(row['Famous Dishes'])
        data_list.append(row['Cuisines'])
        data_list.append(row['Approx cost(for two people)'])
        data_list.append(row['Type'])
        final_list.append(data_list)
    if request.method == 'POST':
        print("Searching !!!")
        find = request.POST['search']
        print(find)
        csv_fp = open('restaurant.csv', 'r')
        reader = csv.DictReader(csv_fp)
        final_list = []
        for row in reader:
            if(find in row['Restaurant Name'] or find.lower() in row['Restaurant Name'] or find.capitalize() in row['Restaurant Name']):
                data_list = []
                data_list.append(row['Restaurant Name'])
                data_list.append(row['Address'])
                data_list.append(row['Online Order'])
                data_list.append(row['Book Table'])
                data_list.append(row['Rate'])
                data_list.append(row['Phone'])
                data_list.append(row['Restaurant Type'])
                data_list.append(row['Famous Dishes'])
                data_list.append(row['Cuisines'])
                data_list.append(row['Approx cost(for two people)'])
                data_list.append(row['Type'])
                final_list.append(data_list)
                # print(row['Number'])

    final_list.sort(key=lambda x: x[4], reverse=True)
    #print(user_row)
    return render(request, 'dashboard.html', {'data': final_list, 'headers': headers})

def filter(request):
    if(request.method == 'POST'):

        ordered = request.POST.get("online_order", None)
        booking_table = request.POST.get("book_table", None)
        res_rate = request.POST.get("Rate", None)
        res_type = request.POST.get("type", None)
        lprice = request.POST.get("price", None)
        print("Order : ", ordered)
        print("Book table : ", booking_table)
        print("Rating : ", res_rate)
        print("Typing : ", res_type)
        print("Price : ", lprice)
        if(lprice != None):
            uprice = int(lprice)+200
        else:
            uprice = 1000
            lprice = 0
        if(ordered == None):
            ordered = ""
        if(booking_table == None):
            booking_table = ""
        if(res_rate == None):
            res_rate = '0.0'
        if(res_type == None):
            res_type = ''
        csv_fp = open('restaurant.csv', 'r')
        reader = csv.DictReader(csv_fp)
        headers = [col for col in reader.fieldnames if col != 'Unnamed: 0']
        final_list = []
        for row in reader:
            if(ordered in row['Online Order'] and booking_table in row['Book Table'] and float(res_rate) <= float(row['Rate']) and res_type in row['Restaurant Type'] and int(lprice) <= int(row['Approx cost(for two people)']) < int(uprice)):
                data_list = []
                data_list.append(row['Restaurant Name'])
                data_list.append(row['Address'])
                data_list.append(row['Online Order'])
                data_list.append(row['Book Table'])
                data_list.append(row['Rate'])
                data_list.append(row['Phone'])
                data_list.append(row['Restaurant Type'])
                data_list.append(row['Famous Dishes'])
                data_list.append(row['Cuisines'])
                data_list.append(row['Approx cost(for two people)'])
                data_list.append(row['Type'])
                final_list.append(data_list)

    final_list.sort(key=lambda x: x[4], reverse=True)
    return render(request, 'dashboard.html', {'data': final_list, 'headers': headers})

