from django import forms
from .models import Post, Comment, Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address',
        }),
        help_text='Required. Enter a valid email address.'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., Django, Python, Web Development)',
            'data-role': 'tagsinput',
        }),
        help_text='Separate tags with commas. New tags will be created automatically.',
        label='Tags'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate tags field with existing tags if editing a post
        if self.instance.pk:
            existing_tags = self.instance.tags.all()
            tag_names = ', '.join([tag.name for tag in existing_tags])
            self.fields['tags'].initial = tag_names
    
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
    
    def clean_tags(self):
        tags_string = self.cleaned_data.get('tags', '')
        if not tags_string:
            return []
        
        # Split by comma and clean up each tag
        tag_list = [tag.strip() for tag in tags_string.split(',') if tag.strip()]
        
        # Validate tag names
        for tag in tag_list:
            if len(tag) > 50:
                raise forms.ValidationError(f'Tag "{tag}" is too long. Maximum 50 characters per tag.')
            if len(tag) < 2:
                raise forms.ValidationError(f'Tag "{tag}" is too short. Minimum 2 characters per tag.')
        
        # Remove duplicates while preserving order
        seen = set()
        unique_tags = []
        for tag in tag_list:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_tags.append(tag)
        
        return unique_tags
    
    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        
        # Set author if provided and post is new (no pk yet)
        if user and not post.pk:
            post.author = user
        
        if commit:
            post.save()
            # Handle tags after post is saved (needed for many-to-many relationship)
            self.save_tags(post)
        
        return post
    
    def save_tags(self, post):
        """
        Handle tag creation and association with the post.
        Creates new tags if they don't exist and associates them with the post.
        """
        tag_names = self.cleaned_data.get('tags', [])
        
        # Clear existing tags
        post.tags.clear()
        
        # Process each tag
        for tag_name in tag_names:
            # Get or create tag (case-insensitive)
            tag, created = Tag.objects.get_or_create(
                name__iexact=tag_name,
                defaults={'name': tag_name}
            )
            # Associate tag with post
            post.tags.add(tag)


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
        