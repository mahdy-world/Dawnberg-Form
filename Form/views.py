from django.shortcuts import redirect, render
from django.views.generic import * 
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from .forms import *

# Create your views here.
class FormList(LoginRequiredMixin , ListView):
    login_url = '/auth/login/'
    model = Form
    paginate_by = 100

    def get_queryset(self):
       queryset = self.model.objects.all()
       return queryset



class FormCreate(View):
    login_url = '/auth/login/'
    model = Form
    form_class = MainForm
    template_name = 'Form/form_new.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def post(self,request):
        if request.method=='POST':
            form = self.form_class(request.POST or None)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.created_by = request.user
                myform.save()
                return redirect('Form:Formcreate')
        
    
    def get(self, request):
        form = MainForm(request.POST or None)
        queryset = self.model.objects.all()
       
        return render(request, self.template_name , {'form':form , 'all':queryset} )

