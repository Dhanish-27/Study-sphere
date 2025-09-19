from django.db import models
from django.contrib.auth.models import User
import os


# The below is for professional details of the user
def user_profile_photo_path(instance, filename):
    return f'user_{instance.user.id}/profile_photos/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name=models.TextField(max_length=30,blank=True)
    last_name=models.TextField(max_length=30,blank=True)
    phone=models.TextField(max_length=30,blank=True)
    profile_photo = models.ImageField(upload_to=user_profile_photo_path, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    qualification = models.CharField(max_length=100, blank=True)
    field_of_study = models.CharField(max_length=100, blank=True)
    university = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    experience_years = models.IntegerField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    skills = models.TextField(blank=True)  # Store as comma-separated values
    learning_interests = models.TextField(blank=True)
    career_goal = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_skills_list(self):
        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    
    def add_skill(self, skill):
        skills_list = self.get_skills_list()
        if skill not in skills_list:
            skills_list.append(skill)
            self.skills = ','.join(skills_list)
    
    def remove_skill(self, skill):
        skills_list = self.get_skills_list()
        if skill in skills_list:
            skills_list.remove(skill)
            self.skills = ','.join(skills_list)




# the below is for posting question and replying for questions

class Question(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='replies')
    parent_reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='child_replies')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reply by {self.author} on {self.question}"


# The below is for project vidoes section and it's replies

class project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to="project_videos/{user}")
    thumbnail=models.ImageField(upload_to="project_thumbnail/{user}",null=True)


    def __str__(self):
        return self.title

class project_reply(models.Model):
    post = models.ForeignKey(project, on_delete=models.CASCADE, related_name='pro_reply')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# The below is for posts section

class posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="user_posts/{user}")


    def __str__(self):
        return self.title

class posts_replies(models.Model):
    post = models.ForeignKey(project, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# From here the models are for courses and domains

class Language(models.Model):
    name=models.CharField(max_length=70)

class Domain(models.Model):
    """Main course domain like Java Web Development, Java Software Development"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="course_thumbnails/", blank=True, null=True)
    language=models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category inside a domain (e.g. Frontend Development, Backend Development)"""
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.domain.name} - {self.name}"


class Video(models.Model):
    """Videos inside a category (e.g. HTML Fundamentals, CSS Styling)"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    duration = models.CharField(max_length=50, blank=True, null=True)  # Example: "2 hours"

    def __str__(self):
        return f"{self.title} ({self.video_count} videos)"



# cancelled

# class PostVideo(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Video for {self.post.title}"


