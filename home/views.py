from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from datetime import datetime
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.

# HTML pages

def home(request):
     return render(request, 'home/home.html')

def contact(request):
     
     if request.method == "POST":
          #name = request.POST['name'] or,
          name = request.POST.get('name','')
          email =request.POST.get('email','')
          phone = request.POST.get('phone','')
          desc = request.POST.get('desc','')

          if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(desc) < 4:
               messages.error(request,"Please fill the form correctly!")
          else:
               contact = Contact(name=name,email=email,phone=phone,desc=desc,timeStamp = datetime.now())
               contact.save()
               messages.success(request, 'Your details has been submitted successfully')
          
     return render(request,'home/contact.html')

def about(request):
     return render(request, 'home/about.html')

def search(request):
     query = request.GET.get('query')
     if len(query) > 78:
          allPosts = Post.objects.none() #defining empty queryset
     else:
          allPostsTitle = Post.objects.filter(title__icontains = query)
          allPostsContent = Post.objects.filter(content__icontains = query)

          # merge two queryset in django
          allPosts = allPostsTitle.union(allPostsContent)
          
     #count() in used to find length of query set
     if len(allPosts) == 0:
          messages.warning(request,"No search result found")
     
     context = {'allPosts' : allPosts,'query': query}
     # print(query)
     return render(request, 'home/search.html',context = context)


# Authentication APIs

def handleSignup(request):
     if request.method == 'POST':
          #get the post parameters
          username = request.POST['username']
          firstname = request.POST['firstname']
          lastname = request.POST['lastname']
          email = request.POST['email']
          pass1 = request.POST['pass1']
          pass2 = request.POST['pass2']

          # check for errorneous input

          #username should be under 10 characters
          if len(username) > 10: 
               messages.error(request,'username must be under 10 characters')
               return redirect('home')

          #username should be alphanumeric
          if not username.isalnum(): 
               messages.error(request,'username must contains only letters and numbers')
               return redirect('home')
          
          #passwords should match
          if pass1 != pass2 :
               messages.error(request,'passwords do not match')
               return redirect('home')



          #create the user (from django.contrib.auth.models import User)
          myuser = User.objects.create_user(username,email,pass1)
          myuser.first_name = firstname
          myuser.last_name = lastname
          myuser.save()

          messages.success(request,'Your iCoder account has been successfully created')

          return redirect('home')
     else:
          return HttpResponse('404 - NOT found')

def handleLogin(request):
     if request.method == "POST":
          #collect credentials
          loginusername = request.POST['loginusername']
          loginpassword = request.POST['loginpass']

          user = authenticate(username = loginusername, password = loginpassword)

          if user is not None:
               login(request,user)
               messages.success(request,'Successfully Logged in')
               return redirect('home')
          else:
               messages.error(request,'Invalid credential,please try again')
               return redirect('home')
     else:
          return HttpResponse('404 - NOT found')

def handleLogout(request):
     if request.user.is_authenticated:
          logout(request)
          messages.success(request,"Successfully logged out")
          return redirect('home')
     else:
          return HttpResponse('404-not found')