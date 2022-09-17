from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .forms import AddTodoForm
from .models import Todo
from datetime import date


def validate_password(password1,password2):
    if password1 and password2 and password1 == password2:
        if len(password1) < 8:
            return False
        else:
            return True
    return False


class HomepageView(generic.ListView):
    template_name = 'core/index.html'
    context_object_name = 'items'
    model = Todo
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user).all().order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home'] = True
        return context

class Upcoming(LoginRequiredMixin,generic.ListView):
    model = Todo
    template_name = 'core/upcoming.html'
    context_object_name = 'query'

    def get_queryset(self,**kwargs):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user,done=False,date__gt=date.today()).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming'] = True
        return context

class EditTodo(LoginRequiredMixin,generic.View):
    template_name = 'core/post.html'
    def get(self,request,*args,**kwargs):
        query = get_object_or_404(Todo,pk=kwargs['pk'])
        form = AddTodoForm(instance=query)
        context = {'form':form}
        return render(request,self.template_name,context)
    
    def post(self,request,*args,**kwargs):
        query = get_object_or_404(Todo,pk=kwargs['pk'])
        form = AddTodoForm(request.POST or None,instance=query)
        if form.is_valid():
            form.user= self.request.user
            form.save()
            return HttpResponseRedirect(reverse('home'))
        return self.get(*args,**kwargs)
    

class TodoDetailView(generic.DetailView):
    template_name ='core/detail.html'
    model = Todo
    context_object_name = 'item'

def delete_todo(request,pk):
    query = get_object_or_404(Todo,pk=pk)
    query.delete()
    return HttpResponseRedirect(reverse('home'))

class CreateTodo(generic.View):
    template_name = 'core/post.html'
    def get(self,*args,**kwargs):
        form = AddTodoForm()
        context = {'form':form}
        return render(self.request,self.template_name,context)
    def post(self,request,*args,**kwargs):
        form = AddTodoForm(request.POST)
        if form.is_valid():
            query = Todo(**form.cleaned_data)
            query.user = request.user
            query.save()
        else:
            return self.get(*args,**kwargs)
        context = {'form':form}
        return render(request,self.template_name,context)

class LoginRegisterView(generic.View):
    template_name = 'core/login.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)

    def post(self,request,*args,**kwargs):
        form = request.POST['form_type']
        if form == 'login':
            username = request.POST['username']
            password = request.POST['password'] 
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
            else:
                return self.get(*args,**kwargs)
            return HttpResponseRedirect(reverse('home'))
        else:
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password'] 
            password_2 = request.POST['password1'] 
            if validate_password(password,password_2):
                # create User
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return HttpResponseRedirect(reverse('home'))

            
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

