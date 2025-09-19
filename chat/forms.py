from django import forms
from .models import *



# This class is to get reply from the user 
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your reply...','class':'w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500 transition min-h-[100px] placeholder:text-gray-400'})
        }
        

# This class is to get the project's video and detailes from the user
class PostForm(forms.ModelForm):
    class Meta:
        model = project
        fields = ['title', 'description','video']


class ProfessionalDetailsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_photo', 'bio', 'qualification', 'field_of_study', 
            'university', 'graduation_year', 'job_title', 'company',
            'experience_years', 'industry', 'linkedin_url', 'github_url',
            'portfolio_url', 'skills', 'learning_interests', 'career_goal',
            'first_name', 'last_name', 'phone'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a short description about yourself'}),
            'career_goal': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your career aspirations and goals'}),
            'skills': forms.HiddenInput(),  # Will be handled by JavaScript
            'learning_interests': forms.HiddenInput(),  # Will be handled by JavaScript
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields not required
        for field in self.fields:
            self.fields[field].required = False

# from here the forms for courses
# class LanguageForm(forms.ModelForm):
#     class Meta:
#         model=Language
#         fields=["name"]

# class DomainForm(forms.ModelForm):
#     class Meta:
#         model = Domain
#         fields = ["name", "description", "thumbnail", "total_videos", "total_hours"]
#         widgets = {
#             "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter domain name"}),
#             "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Domain description"}),
#             "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control"}),
#             "total_videos": forms.NumberInput(attrs={"class": "form-control"}),
#             "total_hours": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 18 hours"}),
#         }

# class CategoryForm(forms.ModelForm):
#     class Meta:
#         model = Category
#         fields = ["domain", "name"]
#         widgets = {
#             "domain": forms.Select(attrs={"class": "form-control"}),
#             "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter category name"}),
#         }

# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ["category", "title", "youtube_url", "video_count", "duration"]
#         widgets = {
#             "category": forms.Select(attrs={"class": "form-control"}),
#             "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Video title"}),
#             "youtube_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "YouTube URL"}),
#             "video_count": forms.NumberInput(attrs={"class": "form-control"}),
#             "duration": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 2 hours"}),
#         }


# cancelled

# class MultiVideoUploadForm(forms.Form):
#     videos = forms.FileField(widget=forms.ClearableFileInput())