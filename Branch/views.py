from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from django.views.generic import *
from django.urls import reverse, reverse_lazy
# Create your views here.

# Create your views here.
class BranchList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Branch
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False)
        return queryset



class BranchUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Branch
    form_class = BranchForm
    template_name = 'Branch/branch_edit.html'
    success_url = reverse_lazy('Branch:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Branch" 
        context['action_url'] = reverse_lazy('Branch:BranchUpdate' , kwargs={'pk':self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

class BranchCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Branch
    form_class = BranchForm
    template_name = 'Branch/branch_new.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get(self, request):
        form = BranchForm(request.POST or None)
        queryset = self.model.objects.filter(deleted=False)
        return render(request, self.template_name, {'form': form, 'all': queryset})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None )
            if form.is_valid():
                myform = form.save(commit=False)
                myform.created_by = request.user
                myform.save()
                return redirect('Branch:BranchCreate')

class BranchDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Branch
    form_class = BranchDeleteForm
    template_name = 'Branch/branch_delete.html'
    success_url = reverse_lazy('Branch:BranchList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('Branch:BranchDelete', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
