from django.shortcuts import render, redirect
from django.views.generic import CreateView
from jobs.models import Freelancer, Business, Project
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import BusinessUpdateForm, FreelancerUpdateForm, ProjectForm
from django.contrib import messages
from .filters import *
from invitations.utils import get_invitation_model
from django.core.mail import EmailMessage, get_connection
from django.conf import settings



def home(request):
    if request.user.is_authenticated:
        if request.user.get_freelancer():
            f_id = request.user.get_freelancer().id
            user_profile = request.user.get_freelancer()
            freelancers_matched = Freelancer.objects.all().exclude(id=f_id)[:3]

            projects = Project.objects.all()
            projects_matched = []
            business_matched = []
            for project in projects:
                if len(projects_matched) > 3:
                    break
                if project.programming_languages in user_profile.skills:
                    projects_matched.append(project)
                    business_matched.append(project.owner)

        
        elif request.user.get_business():
            b_id = request.user.get_business().id
            user_profile = request.user.get_business()
            business_matched = Business.objects.all().exclude(id=b_id)[:3]
            projects_matched = Project.objects.all()[:3]
            
            projects = Project.objects.all()
            freelancers = Freelancer.objects.all()
            freelancers_matched = []
            for project in projects:
                if len(freelancers_matched) > 3:
                    break
                if project.owner == user_profile:  
                    for fr in freelancers:
                        if project.programming_languages in fr.skills and fr not in freelancers_matched:
                            freelancers_matched.append(fr)

        context = {
            'freelancers': freelancers_matched,
            'businesses': business_matched,
            'projects': projects_matched
        }
        return render(request, 'jobs/home.html', context)
    else:
        freelancers = Freelancer.objects.all()[:3]
        businesses = Business.objects.all()[:3]
        projects = Project.objects.all()[:3]
        context = {
            'freelancers': freelancers,
            'businesses': businesses,
            'projects': projects
        }
        return render(request, 'jobs/home.html', context)

def faq(request):
    return render(request, 'jobs/FAQ.html')

def FreelancerListViews(request):
    if request.user.is_authenticated:
        if request.user.get_freelancer():
            freelancers = Freelancer.objects.all()
        
        elif request.user.get_business():
            user_profile = request.user.get_business()
            projects = Project.objects.all()
            freelancers = Freelancer.objects.all()

            freelancers_matched_id = []
            freelancers_not_matched_id = []
            for project in projects: # first add freelancers that has the same skill as user's projects
                if project.owner == user_profile:  
                    for fr in freelancers:
                        if project.programming_languages in fr.skills and fr not in freelancers_matched_id:
                            freelancers_matched_id.append(fr.id)
                        elif not project.programming_languages in fr.skills and fr not in freelancers_not_matched_id:
                            freelancers_not_matched_id.append(fr.id)

            freelancers_matched = Freelancer.objects.filter(id__in=freelancers_matched_id)
            freelancers_not_matched = Freelancer.objects.filter(id__in=freelancers_not_matched_id)
            freelancers = freelancers_matched | freelancers_not_matched


    myFilter = FreelancerFilter(request.GET, queryset=freelancers)
    freelancers = myFilter.qs
    context = {
        'object_list': freelancers,
        'myFilter': myFilter
    }
    return render(request, 'jobs/freelancer_list.html', context)

def BusinessListViews(request):
    if request.user.is_authenticated:
        if request.user.get_freelancer():
            user_profile = request.user.get_freelancer()

            projects = Project.objects.all()
            business_original = Business.objects.all()
            businesses_matched = []
            businesses_not_matched = []
            for project in projects:
                if project.programming_languages in user_profile.skills and project.owner.id not in businesses_matched:
                    businesses_matched.append(project.owner.id)

            for business in business_original:
                if business.id not in businesses_matched:
                    businesses_not_matched.append(business.id)
            
            businesses_matched = Business.objects.filter(id__in=businesses_matched)
            businesses_not_matched = Business.objects.filter(id__in=businesses_not_matched)
            businesses = businesses_matched | businesses_not_matched
        elif request.user.get_business():
            businesses = Business.objects.all()

    myFilter = BusinessFilter(request.GET, queryset=businesses)
    businesses = myFilter.qs
    context = {
        'object_list': businesses,
        'myFilter': myFilter
    }
    return render(request, 'jobs/business_list.html', context)

def ProjectListViews(request):
    if request.user.is_authenticated:
        if request.user.get_freelancer():
            user_profile = request.user.get_freelancer()

            original_order_projects = Project.objects.all()
            projects_matched = []
            projects_not_matched = []
            for project in original_order_projects:
                if project.programming_languages in user_profile.skills:
                    projects_matched.append(project.id)
                else:
                    projects_not_matched.append(project.id)
            projects_matched = Project.objects.filter(id__in=projects_matched)
            projects_not_matched = Project.objects.filter(id__in=projects_not_matched)
            projects = projects_matched | projects_not_matched
        elif request.user.get_business():
            projects = Project.objects.all()
    myFilter = ProjectFilter(request.GET, queryset=projects)
    projects = myFilter.qs
    context = {
        'object_list': projects,
        'myFilter': myFilter
    }
    return render(request, 'jobs/project_list.html', context)


class FreelancerCreateView(CreateView):
    model = Freelancer
    fields = ['name', 'profile_pic', 'skills', 'about']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(FreelancerCreateView, self).form_valid(form)
    
class BusinessCreateView(CreateView):
    model = Business
    fields = ['name', 'profile_pic', 'about']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(BusinessCreateView, self).form_valid(form)

def view_business_profile(request, pk):
    business = Business.objects.get(id=pk)
    context = {
        'business': business,
        'projects': Project.objects.filter(owner=business)
    }

    return render(request, 'jobs/other_business_profile.html', context)

def view_freelancer_profile(request, pk):
    # rating = Rating.objects.filter(profile=freelancer, user=request.user).first()
    # freelancer.user_rating = rating.rating if rating else 0

    freelancer = Freelancer.objects.get(id=pk)
    elligible = False
    # specify who can rate this freelancer
    if request.user.is_authenticated:
        projects = Project.objects.all()
        if request.user.get_business():
            for project in projects:
                if project.owner == request.user.get_business() and project.developer == freelancer:
                    elligible = True
                    break
    # specify who can rate this freelancer
    context = {
        'freelancer': freelancer,
        'projects': Project.objects.filter(developer=freelancer),
        'elligible': elligible
    }

    return render(request, 'jobs/other_freelancer_profile.html', context)

def view_project_profile(request, pk):
    if request.user.is_authenticated:
        if request.user.get_freelancer():
            freelancer = request.user.get_freelancer()
            business = None
        elif request.user.get_business():
            business = request.user.get_business()
            freelancer = None
    else:
        freelancer = None
        business = None

    project = Project.objects.get(id=pk)
    context = {
        'freelancer': freelancer,
        'business': business,
        'project': project,
        'user': request.user
    }
    return render(request, 'jobs/project_profile.html', context)

def search(request):
    searched_query = request.GET.get('searched_query')
    if searched_query:
        freelancers = Freelancer.objects.filter(name__icontains=searched_query) # it will return every name that contains searched_query as a substring
        businesses = Business.objects.filter(name__icontains=searched_query)
        projects = Project.objects.filter(name__icontains=searched_query)

        context = {
            'freelancers': freelancers,
            'businesses': businesses,
            'projects': projects,
            'searched_query': searched_query,
        }
        return render(request, 'jobs/home.html', context)
    else:
        context = {}
        return render(request, 'jobs/home.html', context)

def freelancer_report(request, pk):
    freelancer = Freelancer.objects.get(id=pk)
    
    projects_id = []
    all_projects = Project.objects.all()
    for p in all_projects:
        if p.developer == freelancer:
            projects_id.append(p.id)


    projects = Project.objects.filter(id__in=projects_id)

    context = {
        'freelancer': freelancer,
        'user': request.user,
        'projects': projects
    }
    return render(request, 'jobs/freelancer_report.html', context)

def business_report(request, pk):
    business = Business.objects.get(id=pk)

    projects_id = []
    all_projects = Project.objects.all()
    for p in all_projects:
        if p.owner == business:
            projects_id.append(p.id)

    projects = Project.objects.filter(id__in=projects_id)

    context = {
        'business': business,
        'user': request.user,
        'projects': projects
    }
    return render(request, 'jobs/business_report.html', context) # remember to change

def rate(request, profile_id, rating):
    freelancer = Freelancer.objects.get(id=profile_id)
    Rating.objects.filter(profile=freelancer, user=request.user).delete()
    # freelancer.rating_set.create(user=request.user, rating=rating)
    new_rating = Rating(profile=freelancer, user=request.user, rating=rating)
    new_rating.save()
    return view_freelancer_profile(request, profile_id)

def change_status(request, profile_id, project_id, new_status):
    project = Project.objects.get(id=project_id)
    if new_status == 0:
        project.is_complete = False
        project.save()
    else:
        project.is_complete = True
        project.save()
    return freelancer_report(request, profile_id)
    

@login_required
def handle_login(request):
    if request.user.get_freelancer() or request.user.get_business():
        return redirect(reverse_lazy('home'))
    
    return render(request, 'jobs/choose_profile.html', {})

def profile(request):
    if request.user.get_freelancer():
        context = {
            'user': request.user,
            'freelancer': request.user.get_freelancer(),
            'projects': Project.objects.filter(developer=request.user.get_freelancer())
        }
        return render(request, 'jobs/freelancer_profile.html', context)
    elif request.user.get_business():
        context = {
            'user': request.user,
            'business': request.user.get_business(),
            'projects': Project.objects.filter(owner=request.user.get_business())
        }
        return render(request, 'jobs/business_profile.html', context)
    else:
        return redirect(reverse_lazy('handle-login'))
    
def update_business(request):
    if request.method == 'POST':
        u_form = BusinessUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.get_business())
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse_lazy('profile'))

    else:
        u_form = BusinessUpdateForm(instance=request.user.get_business())

    context = {
        'u_form': u_form
    }

    return render(request, 'jobs/business_update.html', context)

def update_freelancer(request):
    if request.method == 'POST':
        u_form = FreelancerUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.get_freelancer())
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(reverse_lazy('profile'))

    else:
        u_form = FreelancerUpdateForm(instance=request.user.get_freelancer())

    context = {
        'u_form': u_form
    }

    return render(request, 'jobs/freelancer_update.html', context)

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.owner = self.request.user.get_business()
        return super(ProjectCreateView, self).form_valid(form)
    

def accept_project(request, pk):
    freelancer = request.user.get_freelancer()
    Project.objects.filter(id=pk).update(developer=freelancer)
    return redirect(reverse_lazy('profile'))

def invite(request):
    Invitation = get_invitation_model()
    # sender = request.user.email
    receiver = request.GET.get('invitation')
    invite = Invitation.create(receiver, inviter=request.user)
    link = f'http://localhost:8000/invitations/accept-invite/{invite.key}'
    invite_msg = f'Hello, You ({receiver}) have been invited to join Green Minds. If you would like to join, please go to {link}'
    subject = 'Invitation to join Green Minds'
    # send_mail(subject, invite_msg, sender, [receiver, receiver])
    with get_connection(  
        host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
        username=settings.EMAIL_HOST_USER, 
        password=settings.EMAIL_HOST_PASSWORD, 
        use_tls=settings.EMAIL_USE_TLS  
       ) as connection:  
           subject = subject  
           email_from = settings.EMAIL_HOST_USER  
           recipient_list = [receiver, ]  
           message = invite_msg
           EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()
    invite.send_invitation(request)
    return redirect(reverse_lazy('profile'))



