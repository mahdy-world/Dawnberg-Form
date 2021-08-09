from django.shortcuts import redirect, render
from django.views.generic import * 
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from .forms import *
from django.urls import reverse_lazy

# Create your views here.
class FormList(LoginRequiredMixin , ListView):
    login_url = '/auth/login/'
    model = Form
    paginate_by = 100

    def get_queryset(self):
       queryset = self.model.objects.all()
       return queryset



class FormCreate(LoginRequiredMixin ,CreateView):
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
                return redirect('Form:FormView' , pk=myform.id)
        
    
    def get(self, request):
        form = MainForm(request.POST or None)
        queryset = self.model.objects.all()
       
        return render(request, self.template_name , {'form':form , 'all':queryset} )

class FormUpdate(LoginRequiredMixin , UpdateView):
    login_url = '/auth/login/'
    model = Form
    form_class = MainForm
    template_name = 'Form/form_new.html'
    success_url = reverse_lazy('Form:FormUpdate')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('Form:update' , kwargs={'pk':self.object.id})

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            self.success_url    


class FormView(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Form
    template_name = 'Form/form_view.html'
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        kwargs['forms'] = Form.objects.get(id=self.kwargs['pk'])
        kwargs['question'] = Question.objects.filter(form=self.kwargs['pk'])
        return super(FormView , self).get_context_data(**kwargs)

        
        
    

    


class QuestionCreate(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = Question
    form_class = QuestionForm
    template_name = 'Question/Question_new.html'
    success_url = reverse_lazy('Form:FormList')
    

    

    def get_queryset(self):
        queryset = self.model.objects.get()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = OptionsFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OptionsFormSet()
        return context

    def form_valid(self, form):
        myform = form.save(commit=False)
        myform.form = Form.objects.get(id=self.kwargs['pk'])
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            myform.save()
            self.object = myform
            formset.instance = self.object
            formset.save()
        return redirect(self.success_url)
'''
    def post(self,request,pk):
        form = self.form_class(request.POST or None)
        if request.method=='POST':
            form = self.form_class(request.POST or None)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.form = Form.objects.get(id=pk)
    
                return redirect('Form:QuestionCreate', pk=pk)

        return render(request, self.template_name , {'form':form })    
 '''
    

    # def get(self, request ):
    #     form = self.form_class(request.POST or None)
    #     queryset = self.model.objects.all()
       
    #     return render(request, self.template_name , {'form':form , 'all':queryset} )    

    
  