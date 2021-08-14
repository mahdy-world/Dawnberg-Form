from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from django.views.generic import *
from django.urls import reverse, reverse_lazy
# Create your views here.

class EmployeeCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee_new.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get(self, request):
        form = EmployeeForm(request.POST or None)
        queryset = self.model.objects.all()
        return render(request, self.template_name, {'form': form, 'all': queryset})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None , request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.created_by = request.user
                myform.save()
                return redirect('Employee:EmployeeCreate')

    
    