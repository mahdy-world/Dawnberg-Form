from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from .forms import *
from django.urls import reverse, reverse_lazy


# Create your views here.
class FormList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Form
    paginate_by = 100

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset


class FormCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Form
    form_class = MainForm
    template_name = 'Form/form_new.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None)
            if form.is_valid():
                myform = form.save(commit=False)
                myform.created_by = request.user
                myform.save()
                return redirect('Form:FormView', pk=myform.id)

    def get(self, request):
        form = MainForm(request.POST or None)
        queryset = self.model.objects.all()

        return render(request, self.template_name, {'form': form, 'all': queryset})


class FormUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Form
    form_class = MainForm
    template_name = 'Form/form_edit.html'
    success_url = reverse_lazy('Form:FormView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('Form:FormUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        return reverse('Form:FormView', kwargs={'pk': self.object.id})


class FormView(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Form
    template_name = 'Form/form_view.html'
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        kwargs['forms'] = Form.objects.get(id=self.kwargs['pk'])
        kwargs['question'] = Question.objects.filter(form=self.kwargs['pk'])
        return super(FormView, self).get_context_data(**kwargs)


class OptionalQuestionCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Question
    form_class = QuestionForm
    template_name = 'Question/Question_new.html'

    def get_success_url(self):
        return reverse_lazy('Form:FormView', kwargs={'pk': self.request.POST.get('form_pk')})

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
        return redirect(self.get_success_url())


class TextQuestionCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Question
    form_class = QuestionForm
    template_name = 'Question/Question_new.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:FormView', kwargs={'pk': self.request.POST.get('form_pk')})

    def form_valid(self, form):
        question = form.save(commit=False)
        question.form = Form.objects.get(id=self.request.POST.get('form_pk'))
        question.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pk'] = self.request.GET.get('form_id')
        return context


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


class TextQuestionUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Question
    form_class = QuestionForm
    template_name = 'Question/Question_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pk'] = self.request.GET.get('form_id')
        context['action_url'] = reverse_lazy('Form:TextQuestionUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:FormView', kwargs={'pk': self.object.form_id})


class OptionQuestionUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Question
    form_class = QuestionForm
    template_name = 'Question/Question_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = OptionsFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OptionsFormSet()
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pk'] = self.request.GET.get('form_id')
        context['action_url'] = reverse_lazy('Form:TextQuestionUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:FormView', kwargs={'pk': self.object.form_id})


def guest_form(request, pk):
    context = {

    }
    if request.method == 'GET':
        form = Form.objects.get(id=pk)
        instance = Instance.objects.create(form=Form.objects.get(id=pk))
        questions = Question.objects.filter(form=form)
        context.update({
            'instance': instance,
            'questions': questions,
            'form': form,
        })
        return render(request, 'Answer/answer_page.html', context)
    if request.method == 'POST':
        optional_dict = {}
        for question, answer in request.POST.items():
            if question == 'instance':
                instance = Instance.objects.get(id=answer)
                print('instance')
                continue
            if question == 'csrfmiddlewaretoken':
                print('csrfmiddlewaretoken')
                continue
            if answer != 'on':
                # Text Question
                question_object = Question.objects.get(id=question)
                answer_object = Answer()
                answer_object.instance = instance
                answer_object.question = question_object
                answer_object.text_answer = answer
                answer_object.save()
            else:
                # Optional Question
                q = question[:-1]
                question_object = QuestionOption.objects.get(id=q).question
                # check if there is old options in optional_dict for this question
                if str(question_object.id) in optional_dict.keys():
                    old_value = optional_dict[str(question_object.id)]
                    new = ',' + q
                    optional_dict[str(question_object.id)] += new
                    new_value = optional_dict[str(question_object.id)]
                    optional_dict.update({str(question_object.id): new_value})
                else:
                    optional_dict.update({str(question_object.id): q})

        for question, question_answer in optional_dict.items():
            answer_object = Answer()
            answer_object.instance = instance
            answer_object.question = Question.objects.get(id=question)
            answer_object.optional_answer = question_answer
            answer_object.save()
        instance.is_submitted = True
        instance.save()
        return redirect('Form:thankyou')

    return render(request, 'Answer/answer_page.html', context)


def thank_you(request):
    return render(request, 'Answer/thankyou.html')


def add_call(request, pk):
    instance = get_object_or_404(Instance, id=pk)
    form = CallForm(request.POST or None)
    if form.is_valid():
        call = form.save(commit=False)
        call.employee = request.user
        call.instance = instance
        call.save()
        return redirect('Form:AnswerList', pk=instance.form.id)
    context = {
        'form': form
    }
    return render(request, 'Answer/add_call.html', context)


def add_comment(request, pk):
    instance = get_object_or_404(Instance, id=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.instance = instance
        comment.save()
        return redirect('Form:AnswerList', pk=instance.form.id)
    context = {
        'form': form
    }
    return render(request, 'Answer/add_comment.html', context)


# def  convert(request ,pk):
#     instance_id = get_object_or_404(Form , id=pk)
#     form = ConvertForm(request.POST or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.form = instance_id
#         instance.save()
#         return redirect('Form:AnswerList' , pk=instance.form.id)
#     context = {
#         'form':form
#     }    
#     return render(request, 'Answer/covert.html' , context)
class CallUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = InstanceCall
    form_class = CallForm
    template_name = 'Answer/update_call.html'
    success_url = reverse_lazy('Form:CallUpdate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('Form:CallUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:AnswerList', kwargs={'pk': self.object.instance.form.id})


class CommentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = InstanceComment
    form_class = CommentForm
    template_name = 'Answer/update_comment.html'
    success_url = reverse_lazy('Form:CommentUpdate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('Form:CommentUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:AnswerList', kwargs={'pk': self.object.instance.form.id})


class Convert(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Instance
    form_class = ConvertForm
    template_name = 'Answer/convert.html'
    success_url = reverse_lazy('Form:Convert')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_url'] = reverse_lazy('Form:Convert', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:AnswerList', kwargs={'pk': self.object.form.id})


def take(request, pk):
    if request.method == "POST":
        instance = Instance.objects.get(id=request.POST.get("take"))
        instance.assigned_employee = request.user
        instance.save()
        return redirect('Form:AnswerList', pk=instance.form.id)


class AnswerList(DetailView):
    model = Form
    template_name = 'Answer/answer_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instances'] = Instance.objects.filter(form=self.object, is_submitted=True)
        return context
