# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required






# The below is the def for index page
@login_required
def index(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    All_posts = posts.objects.all().order_by('-created_at')
    all_questions = Question.objects.all().order_by('-created_at')
    all_projects = project.objects.all().order_by('-created_at')

    return render(request, 'professional_index_page.html', {
        'posts': All_posts,
        'questions': all_questions,
        'projects': all_projects,
        'profile': profile
    })

# The below 3 are for creating questions, posts and projects
@login_required
def create_question(request):
    if request.method=="POST":
        title=request.POST.get('title')
        body=request.POST.get('body')
        Question.objects.create(title=title,body=body,author=request.user)
        return redirect("index")
    return render(request,'all_upload_form.html')


@login_required
def create_post(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        image=request.FILES.get("image")
        posts.objects.create(title=title,description=description,image=image,user=request.user)
        return redirect("index")
    return render(request,'all_upload_form.html')

@login_required
def create_project(request):
    if request.method=="POST":
        print("This is inside post")
        title=request.POST.get("title")
        description=request.POST.get("description")
        video=request.FILES.get("video")
        thumbnail=request.FILES.get("thumbnail")
        project.objects.create(user=request.user,title=title,description=description,video=video,thumbnail=thumbnail)
        return redirect("index")
    return render(request,'all_upload_form.html')

# The below is for viewing a single question in a whole page with replies

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    replies = question.replies.filter(parent_reply__isnull=True).order_by('-created_at')
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.question = question
            reply.author = request.user
            reply.save()
            return redirect('question_detail', pk=pk)
    else:
        form = ReplyForm()

    return render(request, 'comments.html', {
        'question': question,
        'replies': replies,
        'form': form,
    })


# The below is for fetching all the available posts
from django.core.paginator import Paginator
from django.http import JsonResponse

def all_posts(request):
    posts_queryset = posts.objects.all().order_by('-created_at')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts_queryset, 10)  # 10 posts per page

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Ajax request
        page_obj = paginator.get_page(page_number)
        posts_data = []
        for post in page_obj:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'description': post.description,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user': post.user.username,
                'image': post.image.url if post.image else None,
            })
        return JsonResponse({
            'posts': posts_data,
            'has_next': page_obj.has_next(),
        })
    else:
        # Initial page load
        page_obj = paginator.get_page(page_number)
        return render(request, 'posts.html', {'posts': page_obj})


# The below functions are for adding courses and its details

def add_language(request):
    language=Language.objects.all()
    domains=Domain.objects.all()
    categories=Category.objects.all()
    if request.method == "POST":
        lang_name = request.POST.get("language")   
        if lang_name:
            Language.objects.create(name=lang_name)
        return redirect("add_language")
    return render(request, "course form.html",{"language":language,"domains":domains,"categories":categories})


def add_domain(request):
    language=Language.objects.all()
    domains=Domain.objects.all()
    categories=Category.objects.all()
    if request.method == "POST":
        name = request.POST.get("domain_name")        
        desc = request.POST.get("domain_desc")        
        thumb = request.FILES.get("domain_thumbnail") 
        lang_id = request.POST.get("domain_language") 

        if lang_id:  # foreign key check
            lang = get_object_or_404(Language, id=lang_id)
            Domain.objects.create(
                name=name,
                description=desc,
                thumbnail=thumb,
                language=lang
            )
        return redirect("add_language")
    return render(request, "course form.html",{"language":language,"domains":domains,"categories":categories})


def add_category(request):
    language=Language.objects.all()
    domains=Domain.objects.all()
    categories=Category.objects.all()
    if request.method == "POST":
        domain_id = request.POST.get("cat_domain")  
        name = request.POST.get("cat_name")        

        if domain_id:
            domain = get_object_or_404(Domain, id=domain_id)
            Category.objects.create(domain=domain, name=name)
        return redirect("add_language")
    return render(request, "course form.html",{"language":language,"domains":domains,"categories":categories})


def add_video(request):
    language=Language.objects.all()
    domains=Domain.objects.all()
    categories=Category.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("vid_category") 
        title = request.POST.get("vid_title")          
        url = request.POST.get("vid_url")              
        duration = request.POST.get("vid_duration")    

        if category_id:
            category = get_object_or_404(Category, id=category_id)
            Video.objects.create(
                category=category,
                title=title,
                youtube_url=url,
                duration=duration
            )
        return redirect("add_language")
    return render(request, "course form.html",{"language":language,"domains":domains,"categories":categories})






# Professional Details View
@login_required
def professional_details(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Update profile fields directly from POST data
        profile.first_name = request.POST.get('first_name', '')
        profile.last_name = request.POST.get('last_name', '')
        profile.phone = request.POST.get('phone', '')
        profile.bio = request.POST.get('bio', '')
        profile.qualification = request.POST.get('qualification', '')
        profile.field_of_study = request.POST.get('field_of_study', '')
        profile.university = request.POST.get('university', '')
        profile.graduation_year = request.POST.get('graduation_year') or None
        profile.job_title = request.POST.get('job_title', '')
        profile.company = request.POST.get('company', '')
        profile.experience_years = request.POST.get('experience_years') or None
        profile.industry = request.POST.get('industry', '')
        profile.linkedin_url = request.POST.get('linkedin_url', '')
        profile.github_url = request.POST.get('github_url', '')
        profile.portfolio_url = request.POST.get('portfolio_url', '')
        profile.skills = request.POST.get('skills', '')
        profile.learning_interests = request.POST.get('learning_interests', '')
        profile.career_goal = request.POST.get('career_goal', '')
        profile.certifications = request.POST.get('certifications') or 0
        
        # Handle profile photo upload
        if 'profile_photo' in request.FILES:
            profile.profile_photo = request.FILES['profile_photo']
        
        profile.save()
        return redirect('profile_page')
    
    return render(request, 'professional_details_form.html', {
        'profile': profile
    })

# Profile Page View
@login_required
def profile_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_posts = posts.objects.filter(user=request.user).order_by('-created_at')
    user_projects = project.objects.filter(user=request.user).order_by('-created_at')
    user_questions = Question.objects.filter(author=request.user).order_by('-created_at')
    user_replies = Reply.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'profile': profile,
        'posts': user_posts,
        'projects': user_projects,
        'questions': user_questions,
        'replies': user_replies,
        'num_posts': user_posts.count(),
        'num_projects': user_projects.count(),
        'num_questions': user_questions.count(),
        'num_replies': user_replies.count(),
        'certifications': profile.certifications,
    }
    return render(request, 'profile page.html', context)

# My Projects View
@login_required
def my_projects(request):
    user_projects = project.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'projects': user_projects,
    }
    return render(request, 'my_projects_new.html', context)

# My Posts View
@login_required
def my_posts(request):
    user_posts = posts.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'posts': user_posts,
    }
    return render(request, 'my_posts_new.html', context)

# My Courses View
@login_required
def my_courses(request):
    # Assuming there's a model for user courses or enrollments
    # For now, we'll display a placeholder
    context = {
        'courses': [],  # Placeholder for user's enrolled courses
    }
    return render(request, 'my_courses_new.html', context)
