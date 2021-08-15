from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from django.views.generic import *
from django.urls import reverse, reverse_lazy
# Create your views here.


class EmployeeList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Employee
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        return queryset

class EmployeeCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeForm
    template_name = 'Employee/employee_new.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get(self, request):
        form = EmployeeForm(request.POST or None)
        queryset = self.model.objects.filter(deleted=False)
        return render(request, self.template_name, {'form': form, 'all': queryset})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None , request.FILES)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.created_by = request.user
                myform.save()
                return redirect('Employee:EmployeeCreate')


class EmployeeUpdate(LoginRequiredMixin , UpdateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeForm
    template_name = 'Employee/employee_edit.html'
    success_url = reverse_lazy('Employee:EmployeeProfile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Employee'
        context['action_url'] = reverse_lazy('Employee:EmployeeUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'pk': self.object.id})

        
class EmployeeDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Employee
    form_class = EmployeeDeleteForm
    template_name = 'Forms/form_template.html'
    success_url = reverse_lazy('Employee:EmployeeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['action_url'] = reverse_lazy('Employee:EmployeeDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class EmployeeProfile(LoginRequiredMixin,DeleteView):
    login_url = '/auth/login/'
    model = Employee
    template_name = 'Employee/employee_profile.html'

    def get_context_data(self, **kwargs):
        kwargs['employee'] = Employee.objects.get(id=self.kwargs['pk'])
        return super(EmployeeProfile, self).get_context_data(**kwargs)   