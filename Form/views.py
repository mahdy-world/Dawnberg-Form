from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import *
from .models import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import View
from .forms import *
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


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
        context = super().get_context_data(**kwargs)
        context['forms'] = Form.objects.get(id=self.kwargs['pk'])
        context['question'] = Question.objects.filter(form=self.kwargs['pk'])
        context['text_question_ids'] = [1, 2, 5, 6]
        return context


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

    def get_initial(self):
        initial = super().get_initial()
        question_type = self.request.GET.get('type')
        if question_type:
            initial['question_type'] = int(question_type)
        return initial


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

    def get_initial(self):
        initial = super().get_initial()
        question_type = self.request.GET.get('type')
        if question_type:
            initial['question_type'] = int(question_type)
        return initial

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

    def get_success_url(self, **kwargs):
        return reverse_lazy('Form:FormView', kwargs={'pk': self.object.form_id})


def guest_form(request, pk):
    context = {

    }
    if request.method == 'GET':
        form = Form.objects.get(id=pk)
        instance = Instance.objects.create(form=Form.objects.get(id=pk))
        questions = Question.objects.filter(form=form)
        text_fields = [1, 2, 5, 6]
        context.update({
            'instance': instance,
            'questions': questions,
            'form': form,
            'text_fields': text_fields,
        })
        return render(request, 'Answer/answer_page.html', context)
    if request.method == 'POST':
        for question, answer in request.POST.items():
            if question == 'instance':
                instance = Instance.objects.get(id=answer)
                continue
            if question == 'csrfmiddlewaretoken':
                continue
            else:
                question_object = Question.objects.get(id=question)
                answers_count = Answer.objects.filter(question=question_object, instance=instance).count()
                if answers_count >= 1:
                    continue
                # Text Question
                if question_object.question_type in [1, 2, 5, 6]:
                    answer_object = Answer()
                    answer_object.instance = instance
                    answer_object.question = question_object
                    answer_object.text_answer = answer
                    answer_object.save()
                # Optional Question
                else:
                    if question_object.question_type == 4:
                        # One From Multi-Choice
                        answer_object = Answer()
                        answer_object.instance = instance
                        answer_object.question = question_object
                        answer_object.text_answer = QuestionOption.objects.get(id=answer).option
                        answer_object.save()
                    else:
                        # Multi-Choice
                        select_options = request.POST.getlist(str(question))
                        st = ''
                        for option in select_options:
                            if st == '':
                                st += QuestionOption.objects.get(id=int(option)).option
                            else:
                                st += ',' + QuestionOption.objects.get(id=int(option)).option
                        answer_object = Answer()
                        answer_object.instance = instance
                        answer_object.question = question_object
                        answer_object.text_answer = st
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
    if instance.status:
        form.fields['instance_status'].initial = instance.status
    if form.is_valid():
        call = form.save(commit=False)
        call.employee = request.user
        call.instance = instance
        call.save()
        if form.cleaned_data['instance_status']:
            instance.status = form.cleaned_data['instance_status']
            instance.save()
        history = CallHistory()
        history.instance = instance
        history.call_by = request.user
        history.call = call
        history.call_type = 1
        history.save()
        message = "تم اضافة مكالمة بنجاح"
        context = {
            'message': message
        }
        return redirect('Form:AnswerList', pk=instance.form.id)

    # return history call for instance using id 
    call_history = CallHistory.objects.filter(instance=instance).order_by('-add_at')

    context = {
        'form': form,
        'call_history': call_history
    }

    return render(request, 'Answer/add_call.html', context)


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
        'form': form,
        'instance': instance
    }
    return render(request, 'Answer/add_comment.html', context)


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
    template_name = 'Answer/answer_card_list.html'

    def post(self, request, *args, **kwargs):
        selected_items = []
        action = ''
        for instance_id, selected in request.POST.items():
            if instance_id == 'action':
                action = selected
                continue
            selected_items.append(instance_id)
        selected_items.remove('csrfmiddlewaretoken')
        instances = Instance.objects.filter(id__in=selected_items)
        message = 'تم'
        if action == 'delete':
            instances.update(deleted=True)
            message += ' حذف عدد: '
        elif action == 'restore':
            instances.update(deleted=False)
            message += 'إستعادة عدد: '

        message += str(instances.count())
        message += 'إجابات'
        messages.add_message(request, messages.SUCCESS, message)
        print(message)
        return redirect(reverse_lazy('Form:AnswerList', kwargs=kwargs))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('is_trash') == '1':
            instances = Instance.objects.filter(deleted=True, form=self.object, is_submitted=True)
        else:
            instances = Instance.objects.filter(deleted=False, form=self.object, is_submitted=True)
        if not self.request.user.has_perms(''):
            instances = instances.filter(assigned_employee=self.request.user)
        if self.request.GET.get('q'):
            instances = instances.filter()
        context['instances'] = instances
        return context


class CallDetail(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = InstanceCall
    template_name = 'Answer/call_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kwargs['call'] = InstanceCall.objects.get(id=self.kwargs['pk'])
        return super(CallDetail, self).get_context_data(**kwargs)


class QuestionDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Question
    form_class = QuestionForm

    def get_success_url(self):
        return reverse_lazy('Form:FormView', kwargs={'pk': self.object.form.id})

    def get_template_names(self):
        if self.object.deleted:
            return 'forms/restore_form.html'
        else:
            return 'forms/delete_form.html'


def assign_to_me(request, pk):
    instance = Instance.objects.get(id=pk)
    instance.assigned_employee = request.user
    instance.save()
    return redirect('Form:AnswerList', instance.form.id)


def delete_instance(request, pk):
    instance = Instance.objects.get(id=pk)
    form = InstanceDeleteForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('Form:AnswerList', instance.form.id)
    context = {
        'instance': instance,
        'form': form,
    }
    if instance.deleted:
        return render(request, 'forms/restore_form.html', context)
    else:
        return render(request, 'forms/delete_form.html', context)


class StatusList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Status
    paginate_by = 30
    template_name = 'Status/status_list.html'

    def get_queryset(self):
        return self.model.objects.filter(deleted=False)


class StatusCreate(LoginRequiredMixin, CreateView):
    login_url = 'auth/login/'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('Form:StatusList')
    template_name = 'Status/form.html'


class StatusUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'auth/login/'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('Form:StatusList')
    template_name = 'Status/form.html'


class StatusDelete(LoginRequiredMixin, UpdateView):
    login_url = 'auth/login/'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('Form:StatusList')
    template_name = 'forms/delete_form.html'


class InstanceStatusUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'auth/login/'
    model = Instance
    form_class = ChangeInstanceStatusForm
    success_url = reverse_lazy('Form:AnswerList')
    template_name = 'Answer/convert.html'
