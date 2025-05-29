from django import forms
from .models import Question
from .models import PollComment, Question  # import all models you use in forms.py


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': forms.SelectDateWidget(years=range(2020, 2030))
        }

#form for users to submit comments on polls
class PollCommentForm(forms.ModelForm):
    class Meta:
        model = PollComment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
# This form allows users to submit comments on polls.
# It includes a text area for the comment text and can be used in the view
# to handle comment submissions.
# This form can be extended with additional fields or validation as needed.
# For example, you might want to limit the length of the comment or
# restrict certain characters. You can also add custom validation methods
# to ensure the comment meets specific criteria before saving it to the database.
# This can help improve the quality of comments and prevent spam or inappropriate content.
# Additionally, you can customize the form's appearance using CSS classes
# or JavaScript to enhance the user experience.
# This can include features like real-time character count, emoji support,
# or markdown formatting for comments. You can also integrate this form
# with a rich text editor to allow users to format their comments more easily.
# This can help create a more engaging and interactive discussion environment
# for users, encouraging them to participate and share their thoughts on the polls.