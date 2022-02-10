from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Feedback, Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm
from django.urls import reverse



class AccessMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blogapp/home.html', context)


def about(request):
    return render(request, 'blogapp/about.html', { 'title' : 'About page'})


def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class PostListView(ListView):
    model = Post
    template_name = 'blogapp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post

#Comment Section

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = Post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)

# Likes section ---------------------------------------

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        post: Post = self.object
        feedbacks = post.feedbacks.all()
        data['number_of_likes'] = len(feedbacks.filter(feedback__status=1))
        data['dislikes'] = len(feedbacks.filter(feedback__status=0))

        data['post_is_liked'] = self.request.user in feedbacks
        return data

# -------------------------------------------------------------

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(AccessMixin, UpdateView):
    model = Post
    fields = ["title", "content", 'tags']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
           
class PostDeleteView(AccessMixin, DeleteView):
    model = Post
    success_url = '/'




    
