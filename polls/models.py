from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class UserVote(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')

#add a model for poll comments and discussion
class PollComment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # New field (alteration)

    def __str__(self):
        return f"{self.user.username}: {self.comment_text[:20]}..."
# This model allows users to comment on polls and discuss them.
# It includes a foreign key to the Question model, a foreign key to the User model,
# a text field for the comment, and a timestamp for when the comment was created.
# This can be used to create a discussion thread for each poll.