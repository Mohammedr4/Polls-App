from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Choice, UserVote, PollComment
from .forms import QuestionForm  # Make sure you have this form defined

# Index view that lists the latest 5 questions
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

# Detail view to show a specific question and its choices
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()

        # Get comments for this question, ordered by newest first
        comments = PollComment.objects.filter(question=question).order_by('-created_at')
        context['comments'] = comments

        # Check if the user has voted on this question
        has_voted = UserVote.objects.filter(user=self.request.user, question=question).exists()
        context['has_voted'] = has_voted
        return context

# Results view showing poll results
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# Vote view: record vote if not voted before, else show error
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

# Create a new question
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

# Add a comment to a poll question
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
