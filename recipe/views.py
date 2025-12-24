from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login/")
def recipe(request):

    if request.method == "POST":
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        print(recipe_name)

        Recipe.objects.create(

            recipe_name = recipe_name,
            recipe_description = recipe_description,
            recipe_image = recipe_image
        )

        return redirect("/")
    
    
    queryset = Recipe.objects.all()
    back = False

    if request.GET.get("search"):

        queryset = queryset.filter(recipe_name__icontains = request.GET.get("search"))
        back = True


    context = {"recipes":queryset, "back_check":back}
    return render(request,"index.html", context)

@login_required(login_url="/login/")
def delete_recipe(request, id):

    queryset = Recipe.objects.get(id = id)
    queryset.delete()
    return redirect("/")

@login_required(login_url="/login/")
def update_recipe(request, id):

    queryset = Recipe.objects.get(id = id)
    
    if request.method == "POST":
      
        queryset.recipe_name = request.POST.get("recipe_name")
        queryset.recipe_description = request.POST.get("recipe_description")

        if request.FILES.get("recipe_image"):
            queryset.recipe_image = request.FILES.get("recipe_image")
        
        queryset.save()
        
        return redirect("/")
    
    context = {"recipe":queryset}
    return render(request, "update.html",context)

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username!")
            return redirect("/login/")
        
        user = authenticate(username = username, password = password)
        
        if not user:
            messages.error(request, "Invalid Password!")
            return redirect("/login/")
        login(request, user)
        return redirect("/")


    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("/login/")

def register_page(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")       
        password = request.POST.get("password")


        user = User.objects.filter(username = username)
        if user.exists():
            messages.error(request, "Username already exists!")
            return redirect("/register/")


        user = User.objects.create(

            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully.")
        return redirect("/register/")
    

    return render(request, "register.html")