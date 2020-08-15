from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView 
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# rewrite this as ListView
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)

# to list all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html, tell ListView which template to use
    context_object_name = 'posts' # look for the 'posts' object
    ordering = ['-date_posted'] # look the post from newest to oldest

    # Pagination
    paginate_by = 5

# to list the posts by a certain user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html' 
    context_object_name = 'posts' 
    paginate_by = 5

    def get_queryset(self):
        # in the User model, look for the username = url, return 404 if not found 
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # return the posts written only by that User
        return Post.objects.filter(author=user).order_by('-date_posted')


# to get a specific post
class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        
        # dislay number of likes
        get_likes = get_object_or_404(Post, id=self.kwargs["pk"])
        total_likes = get_likes.total_likes()
        liked = False
        if get_likes.likes.filter(id=self.request.user.id).exists():
            liked = True   
        context["total_likes"] = total_likes
        context["liked"] = liked

        # display number of dislikes
        get_dislikes = get_object_or_404(Post, id=self.kwargs["pk"])
        total_dislikes = get_dislikes.total_dislikes()
        disliked = False
        if get_dislikes.dislikes.filter(id=self.request.user.id).exists():
            disliked = True   
        context["total_dislikes"] = total_dislikes
        context["disliked"] = disliked

        # display comments
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        # comments is the related name with Post
        comments = post.comments.all().order_by('-date_posted')
        # paginate comments
        paginator = Paginator(comments, 5)
        page = self.request.GET.get('page', 1)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        context["comments"] = comments

        # display comment form
        context["comment_form"] = CommentForm()

        return context

# to create a new post
# inherit from LoginRequiredMixin to redirect users to login page when the try to create post not logged in
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content'] # date is set automatically

    # overwrite the form_valid method to tell django the the author is the current logged in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) # run the form_valid method in the parent class

# to update post in the front end
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content'] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

    # make sure that the current user is the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# to delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/' # send the user back to homepage upon successful deletion

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False   

def about(request):
    return render(request, 'blog/about.html', {'title': "About"})

# like the post and save it to database
@login_required
def likeView(request, pk):
    post = get_object_or_404(Post, id=pk)

    liked = False
    # check if the user have already liked the post in the past
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user) # undo the like if users press like button again
        liked = False
    # check if the user have already disliked the post in the past
    elif post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user) # undo the dislike
        post.likes.add(request.user) # add the like
        liked = True
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

# dislike the post and save it to database
@login_required
def dislikeView(request, pk):
    post = get_object_or_404(Post, id=pk)

    disliked = False
    # check if the user have already disliked the post in the past
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user) # undo the dislike if users press dislike button again
        disliked = False
    # check if the user have already liked the post in the past
    elif post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user) # undo the like
        post.dislikes.add(request.user) # add the dislike
        disliked = True
    else:
        post.dislikes.add(request.user)
        disliked = True

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# post comments as saves comments to database
@login_required
def commentView(request, pk, username):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    user = get_object_or_404(User, username=username)

    # comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save()
            # Assign the current post to the comment
            new_comment.post = post
            # Assign the current user to the comment
            new_comment.user = user
            # Save the comment to the database
            new_comment.save()
            messages.success(request, f'Your have added a new comment.')
    else:
        comment_form = CommentForm()
    
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


# to delete a comment
@login_required
def commentDelete(request, pk, id):
    comment = get_object_or_404(Comment, id=pk).delete()
    messages.success(request, f'Your comment is removed.')
    return HttpResponseRedirect(reverse('post-detail', args=[str(id)]))