# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required






# The below is the def for index page
@login_required
def index(request):
    userprofile=UserProfile.objects.all()
    All_posts=posts.objects.all()
    all_questions=Question.objects.all()
    all_projects=project.objects.all()

    return render(request,'show.html',{'posts':All_posts,'questions':all_questions,'projects':all_projects})

# The below 3 are for creating questions, posts and projects
@login_required
def create_question(request):
    if request.method=="POST":
        title=request.POST.get('title')
        body=request.POST.get('body')
        Question.objects.create(title=title,body=body,author=request.user)
        return render(request,'all_upload_form.html')
    return render(request,'all_upload_form.html')


@login_required
def create_post(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        image=request.POST.get('image')
        posts.objects.create(title=title,description=description,image=image,user=request.user)
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
    return render(request,"post_upload.html")

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
def all_posts(request):
    posts=posts.objects.all()
    return render(request,'posts.html',{'posts':posts})


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
        form = ProfessionalDetailsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('professional_details')
    else:
        form = ProfessionalDetailsForm(instance=profile)

    return render(request, 'professional_details_form.html', {
        'form': form,
        'profile': profile
    })
