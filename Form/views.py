from django.shortcuts import redirect, render
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
    form = Form.objects.get(id=pk)
    instance = Instance.objects.create(form=Form.objects.get(id=pk))
    questions = Question.objects.filter(form=form)
    if request.POST:
        optional_dict = {}
        for question, answer in request.POST.items():
            if question == 'csrfmiddlewaretoken':
                continue
            if answer == 'on':
                # Optional Question
                question_object = QuestionOption.objects.get(id=question).question
                if str(question_object.id) in optional_dict.keys():
                    old_value = optional_dict[str(question_object.id)]
                    optional_dict[str(question_object.id)].append(question)
                    new_value = optional_dict[str(question_object.id)]
                    optional_dict.update({str(question_object.id): new_value})
                else:
                    optional_dict.update({str(question_object.id): [question]})
            else:
                # Text Question
                question_object = Question.objects.get(id=question)
                answer_object = Answer()
                answer_object.instance = instance
                answer_object.question = question_object
                answer_object.text_answer = answer
                answer_object.save()
        for question, question_answer in optional_dict.items():
            answer_object = Answer()
            answer_object.instance = instance
            answer_object.question = Question.objects.get(id=question)
            answer_object.optional_answer = question_answer
            answer_object.save()

    context = {
        'instance': instance,
        'questions': questions,
        'form': form,
    }
    return render(request, 'Answer/answer_page.html', context)


# class AnswerView(DetailView):
#     model = Form
#     template_name = 'Answer/answer_page.html'
#     form_class = QuestionForm

#     def get_context_data(self, **kwargs):
#         instance = Instance.objects.create()
#         kwargs['forms'] = Form.objects.get(id=self.kwargs['pk'])
#         kwargs['question'] = Question.objects.filter(form=self.kwargs['pk'])
#         kwargs['instance'] = instance.id

#         return super(AnswerView, self).get_context_data(**kwargs)
