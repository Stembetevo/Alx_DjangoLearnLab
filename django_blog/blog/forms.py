from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'maxlength': '200',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your blog post content here...',
                'rows': 10,
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
        }
        help_texts = {
            'title': 'Maximum 200 characters',
            'content': 'Write your blog post content in detail',
        }
    
    def clean_title(self):
        
        title = self.cleaned_data.get('title')
        if not title or title.strip() == '':
            raise forms.ValidationError('Title cannot be empty.')
        return title.strip()
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError('Content cannot be empty.')
        if len(content.strip()) < 10:
            raise forms.ValidationError('Content must be at least 10 characters long.')
        return content.strip()
    
    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        
        # Set author if provided and post is new (no pk yet)
        if user and not post.pk:
            post.author = user
        
        if commit:
            post.save()
        
        return post


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
            }),
        }
    
    def clean_email(self):
        """
        Validate email is unique (excluding current user).
        """
        email = self.cleaned_data.get('email')
        if email:
            users = User.objects.filter(email=email).exclude(pk=self.instance.pk)
            if users.exists():
                raise forms.ValidationError('This email is already in use.')
        return email
    
    def clean_username(self):
        """
        Validate username is unique (excluding current user).
        """
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username).exclude(pk=self.instance.pk)
        if users.exists():
            raise forms.ValidationError('This username is already taken.')
        return username

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }),
        }
        labels = {
            'content': 'Comment',
        }
        help_texts = {
            'content': 'Share your thoughts on this post',
        }
    
    def clean_content(self):
        #Validate comment content.
        content = self.cleaned_data.get('content')
        if not content or content.strip() == '':
            raise forms.ValidationError('Comment cannot be empty.')
        if len(content.strip()) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        if len(content.strip()) > 1000:
            raise forms.ValidationError('Comment cannot exceed 1000 characters.')
        return content.strip()
    
    def save(self, commit=True, post=None, author=None):
        #Save comment with post and author if provided.
        comment = super().save(commit=False)
        
        # Set post and author if provided and comment is new
        if post and not comment.pk:
            comment.post = post
        if author and not comment.pk:
            comment.author = author
        
        if commit:
            comment.save()
        
        return comment
        