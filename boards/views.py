from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.utils import timezone
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


# Create your views here.


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20
    ordering = ['-last_updated']
    board = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(board=self.board).annotate(replies=Count('posts') - 1)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = NewTopicForm
    template_name = 'new_topic.html'
    board = None

    def dispatch(self, request, *args, **kwargs):
        self.board = get_object_or_404(Board, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.board
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'instance' not in kwargs or kwargs['instance'] is None:
            instance = Topic(board=self.board, starter=self.request.user)
            kwargs['instance'] = instance
        return kwargs


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2
    ordering = ['created_at']
    topic = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(topic=self.topic)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def dispatch(self, request, *args, **kwargs):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_pk'), pk=self.kwargs.get('pk'))
        response = super().dispatch(request, *args, **kwargs)
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        return response


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'reply_topic.html'
    topic = None

    def dispatch(self, request, *args, **kwargs):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs['board_pk'], pk=self.kwargs['pk'])
        response = super().dispatch(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def form_valid(self, form):
        form.instance.topic = self.topic
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        self.topic.last_updated = timezone.now()
        self.topic.save()
        return response

    def get_success_url(self):
        topic_url = self.object.topic.get_absolute_url()
        topic_post_url = '{url}?page={page}#{id}'.format(
            url=topic_url,
            id=self.object.pk,
            page=self.object.topic.get_page_count()
        )
        return topic_post_url


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        topic = self.object.topic
        topic.last_updated = timezone.now()
        topic.save()
        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(created_by=self.request.user)

    def get_success_url(self):
        return self.object.topic.get_absolute_url()
