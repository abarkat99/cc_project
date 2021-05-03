from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        )
    )
    save_post = None

    class Meta:
        model = Topic
        fields = ['subject']

    def _save_post(self):
        Post.objects.create(message=self.cleaned_data['message'], topic=self.instance, created_by=self.instance.starter)

    def save(self, commit=True):
        topic = super().save(commit=commit)
        if commit:
            self._save_post()
        else:
            self.save_post = self._save_post
        return topic


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]
