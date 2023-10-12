import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin

from blog.forms import CategoryForm, CategorySearchForm, PostForm, PostSearchForm, CommentForm, CommentSearchForm, \
    ContactForm
from blog.models import Category, Post, Comment, Vote, ContactUs


# Create your views here.
class CategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/create_category.html'
    success_url = reverse_lazy('add-category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_form'] = CategorySearchForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search_query')
        search_query = self.request.GET.get('search_query')
        if search_query:
            context['categories'] = Category.objects.filter(name__icontains=search_query)
        return context

    def form_valid(self, form):
        user = self.request.user
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        category = Category(users=user, name=name, description=description)
        category.save()
        return HttpResponseRedirect('add_category')


class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/update_category.html'
    success_url = reverse_lazy('add-category')


class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('add-category')


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('all-posts')

    def form_valid(self, form):
        author = self.request.user
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        category = form.cleaned_data['category']
        publish_date = form.cleaned_data['publish_date']
        publish = form.cleaned_data['publish']
        draft = form.cleaned_data['draft']
        image = self.request.FILES.get('image')
        if publish_date is not None:
            if publish_date <= timezone.now().date():
                publish = True
            else:
                publish = False
        if publish:
            publish_date = datetime.date.today()
        if draft:
            publish = False
        post = Post(author=author, title=title, description=description, category=category, publish_date=publish_date,
                    publish=publish, draft=draft, image=image)
        post.save()
        return HttpResponseRedirect(reverse_lazy('add-post'))


class AllPosts(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PostSearchForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search_query')
        search_query = self.request.GET.get('search_query')
        if search_query:
            context['posts'] = Post.objects.filter(title__icontains=search_query)

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(author=user)
        return queryset


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'
    success_url = reverse_lazy('all-posts')


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('all-posts')


class ViewPost(DetailView):
    model = Post
    template_name = 'blog/front_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['object']
        context['comment_form'] = CommentForm(self.request.POST)
        context['comments'] = post.comments.all()
        context['upvotes'] = post.votes.filter(vote=True).count()
        context['downvotes'] = post.votes.filter(vote=False).count()
        return context

    def post(self, request, slug):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        comment_form = context['comment_form']
        post = context['object']
        user = self.request.user
        parent_comment = request.POST.get('parent_comment')
        reply = request.POST.get('reply')
        if reply != '' or None:
            form = Comment(user=user, post=post, parent_comment=parent_comment, comment=reply)
            form.save()
            return HttpResponseRedirect(reverse_lazy('view-post', args=[slug]))
        if user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            if comment_form.is_valid():
                comment = comment_form.cleaned_data['comment']
                if comment is not None:
                    form = Comment(user=user, post=post, comment=comment)
                    form.save()
                return HttpResponseRedirect(reverse_lazy('view-post', args=[slug]))
            return render(request, self.template_name, context)


class VotePost(LoginRequiredMixin, SingleObjectMixin, View):
    model = Post

    def get(self, request, slug, vote):
        self.object = self.get_object()
        user = self.request.user
        if vote == 1:
            save_vote = Vote(user=user, post=self.object, vote=True)
        else:
            save_vote = Vote(user=user, post=self.object, vote=False)
        try:
            save_vote.save()
            messages.add_message(request, messages.INFO, "Your vote has been submitted")
        except ValidationError as exce:
            messages.add_message(request, messages.INFO, str(exce.message))
        return HttpResponseRedirect(reverse_lazy('view-post', args=[slug]))


class AllComments(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'blog/all_comments.html'
    context_object_name = 'comments'
    queryset = Comment.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CommentSearchForm(self.request.GET)
        context['search_query'] = self.request.GET.get('search_query')
        search_query = self.request.GET.get('search_query')
        if search_query:
            context['comments'] = Comment.objects.filter(comment__icontains=search_query)
        return context

    def get_queryset(self):
        queryset = Comment.objects.filter(post__author=self.request.user)
        return queryset


class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'blog/update_comment.html'
    form_class = CommentForm
    success_url = reverse_lazy('all-comments')


class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/confirm_delete_comment.html'
    success_url = reverse_lazy('all-comments')


class Dashboard(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/dashboard.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=user).count()
        context['comments'] = Comment.objects.filter(user=user).count()
        context['upvotes'] = Vote.objects.filter(user=user, vote=True).count()
        context['downvotes'] = Vote.objects.filter(user=user, vote=False).count()
        if context['posts'] != 0:
            context['latest_publish_date'] = Post.objects.filter(author=user, publish=True).order_by('-publish_date')[0]
        else:
            context['latest_publish_date'] = None
        if context['comments'] != 0:
            context['latest_comment'] = Comment.objects.filter(user=user).order_by('-created_on')[:5]
        else:
            context['latest_comment'] = None
        return context

    def form_valid(self, form):
        author = self.request.user
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        category = form.cleaned_data['category']
        publish_date = form.cleaned_data['publish_date']
        publish = form.cleaned_data['publish']
        draft = form.cleaned_data['draft']
        image = form.cleaned_data['image']
        if publish_date is not None:
            if publish_date <= timezone.now().date():
                publish = True
            else:
                publish = False
        if publish:
            publish_date = datetime.date.today()
        if draft:
            publish = False
        post = Post(author=author, title=title, description=description, category=category, publish_date=publish_date,
                    publish=publish, draft=draft, image=image)
        try:
            post.save()
            messages.add_message(self.request, messages.INFO, "Your post has been saved")
        except ValidationError as exception:
            messages.add_message(self.request, messages.INFO, str(exception.message))
        return HttpResponseRedirect(reverse_lazy('dashboard'))


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5
    queryset = Post.objects.all().order_by('-publish_date')


class CategoryPosts(ListView):
    model = Post
    template_name = 'blog/category_wise_posts.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        queryset = Post.objects.filter(category__slug=category_slug)
        return queryset


class ContactView(CreateView):
    model = ContactUs
    form_class = ContactForm
    template_name = 'blog/contact_us.html'
    success_url = reverse_lazy('index')
    success_message = "Your message has been sent successfully. We'll get back to you soon."

    def form_valid(self, form):
        response = super().form_valid(form)
        email_subject = 'New contact form submission'
        email_template = 'email_message.html'
        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        sender_email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        file = form.cleaned_data['file']
        email_context = {
            'subject': email_subject,
            'name': name,
            'phone': phone,
            'email': sender_email,
            'message': message,
            'attachment': file,
        }
        email_content = render_to_string(email_template, email_context)
        recipient_email = 'ranaawaix157@gmail.com'
        email = EmailMessage(email_subject, email_content, sender_email, [recipient_email])
        email.content_subtype = "html"
        if form.cleaned_data['file']:
            email.attach(form.cleaned_data['file'].name, form.cleaned_data['file'].read(),
                         form.cleaned_data['file'].content_type)
        email.send()
        return response
