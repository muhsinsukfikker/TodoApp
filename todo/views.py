from django.shortcuts import render,redirect
from django.views.generic import View
from todo.forms import Userform,Loginform,TodoForm
from django.contrib.auth import authenticate,login,logout
from todo.models import Todos
# Create your views here.

class RegisterView(View):
    def get(self,request, *args, **kwargs):
        form=Userform()
        
        return render(request, 'register.html', {'form':form})

    def post(self,request, *args, **kwargs):
        form=Userform(request.POST)
        if form.is_valid():
            form.save()
            print('registered successfully')
            return redirect('login')
        
        else:
            return render(request, 'register.html', {'form':form})
        

class LoginView(View):
    def get(self,request, *args, **kwargs):
        form=Loginform()
        return render(request, 'login.html', {'form':form})
    
    def post(self,request, *args, **kwargs):
        form=Loginform(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            user_obj=authenticate(request,username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                print('valid')
                return redirect('index')


        print('login failed')
        return render(request, 'register.html', {'form':form})
    
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')



class IndexView(View):
    def get(self,request, *args, **kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user)
        fin_todo=Todos.objects.filter(status='completed',user=request.user).count()
        prog_todo=Todos.objects.filter(status='inprogress',user=request.user).count()

        pen_todo=Todos.objects.filter(status='todo',user=request.user).count()

        
        return render(request, 'index.html',{'form':form,'data':qs,'fin_todo':fin_todo,'prog_todo':prog_todo,'pen_todo':pen_todo})
    
    def post(self,request, *args, **kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect('index')
        else:
            return render(request, 'index.html',{'form':form})
    

class TodoUpdateView(View):
    def get(self,request, *args, **kwargs):
        id=kwargs.get('pk') 
        if 'status' in request.GET:
            value=request.GET.get('status')
            if value =='inprogress':
                Todos.objects.filter(id=id).update(status='inprogress')
            elif value =='completed':
                Todos.objects.filter(id=id).update(status='completed')

        return redirect('index')
                

class TodoDeleteView(View):
    def get(self,request, *args, **kwargs):
        id=kwargs.get('pk') 
        Todos.objects.filter(id=id).delete()
        return redirect('index')
