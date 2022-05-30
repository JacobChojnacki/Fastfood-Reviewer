from turtle import pos
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, ProductReview
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.generic import ListView
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

# Create your views here.

#Pobieramy tag z domyslnym ustawieniem na None
def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 12) # 12 postow na strone, korzystamy z Paginator
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'blog/post/list.html',
                 {'page': page,
                  'posts': posts,
                  'tag': tag})

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 8
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comments = post.comments.filter(active = True)
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')

        review = ProductReview.objects.create(post=post, user=request.user, stars=stars, content=content)
        return redirect("blog:post_detail", year=year, month=month, day=day, post=post)

    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in = post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags')[:8]
    return render(request,'blog/post/detail.html',{"post":post, 'comments':comments,'comment_form': comment_form,
                                                   "similar_posts":similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == "POST":
        my_form = EmailPostForm(request.POST)
        if my_form.is_valid():
            my_form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            #trzeba bedzie dokonczyc subject, message itp
        else:
            my_form.errors
    else:
        my_form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': my_form,
                                                    'sent': sent})

    
