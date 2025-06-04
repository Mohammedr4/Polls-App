from django.shortcuts import render, get_object_or_404, redirect 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Question, Choice, UserVote, PollComment
from .forms import QuestionForm  

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        comments = PollComment.objects.filter(question=question).order_by('-created_at')
        context['comments'] = comments

        if self.request.user.is_authenticated:
            has_voted = UserVote.objects.filter(user=self.request.user, question=question).exists()
        else:
            has_voted = False
        context['has_voted'] = has_voted

        return context

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required(login_url='login')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if UserVote.objects.filter(user=request.user, question=question).exists():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You have already voted.",
            'has_voted': True
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            'has_voted': False
        })

    selected_choice.votes += 1
    selected_choice.save()
    UserVote.objects.create(user=request.user, question=question, choice=selected_choice)
    messages.success(request, "Your vote has been recorded!")
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required(login_url='login')
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Question created successfully.")
            return redirect('polls:index')
    else:
        form = QuestionForm()
    return render(request, 'polls/create_question.html', {'form': form})

@login_required(login_url='login')
def comment_on_poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            PollComment.objects.create(question=question, user=request.user, comment_text=comment_text)
            messages.success(request, "Your comment has been posted!")
        else:
            messages.error(request, "Comment cannot be empty.")
    return HttpResponseRedirect(reverse('polls:detail', args=(question.id,)))

# --- New login/logout views ---

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('polls:index')
