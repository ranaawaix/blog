from django import forms

from blog.models import Post, Category, Comment, ContactUs


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Category Description'}),
        }
        labels = {
            'name': 'Name',
            'description': 'Description',
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'publish_date', 'publish', 'draft', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Post Description'}),
            'category': forms.Select(attrs={'class': 'form-select', 'aria-label': '-----------'}),
            'publish_date': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Select Date', 'id': 'my_date_picker', 'type': 'text'}),
            'publish': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'category': 'Category',
            'publish_date': 'Publish Date',
            'draft': 'Save as draft',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]
        widgets = {
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment...'}),
        }


class CategorySearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search Users', widget=forms.TextInput(
        attrs={'class': 'form-control me-2', 'placeholder': 'Search Category Name'}))


class PostSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search Posts', widget=forms.TextInput(
        attrs={'class': 'form-control me-2', 'placeholder': 'Search Post Title'}))


class CommentSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search Comments', widget=forms.TextInput(
        attrs={'class': 'form-control me-2', 'placeholder': 'Search Comment'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'message', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email...'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number...'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message here...'}),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone Number',
            'message': 'Message',
            'file': 'Attachment',
        }
