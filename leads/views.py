
from ast import Assign
from agents.mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.views import generic

from .forms import CustomUserCreateForm, LeadModelForm, LeadAssignFrom
from .models import Lead

class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = LeadAssignFrom

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def  form_valid(self,form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(pk=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class= CustomUserCreateForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


def landing_page(request):
    return render(request, "landing.html")


class LeadListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "leads/all_leads.html"
    context_object_name = "leads" # by default the context name is object_list but we can override this

    def get_queryset(self):
        user = self.request.user
        if( user.is_organiser ):
            queryset = Lead.objects.filter(
                organisation = user.userprofile,
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation = user.agent.organisation,
                agent__isnull=False
            )
            queryset.filter(agent__user = user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if( user.is_organiser ):
            queryset = Lead.objects.filter(
                organisation = user.userprofile,
                agent__isnull=True 
            )
            context.update({
                "unassigned_leads" : queryset
            })
        
        return context


def list_leads(request):
    leads = Lead.objects.all()
    contaxt = {
        'leads': leads
    }
    return render(request,"leads/all_leads.html",context=contaxt)


class LeadDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name="leads/lead_detail.html"
    context_object_name='lead'

    def get_queryset(self):
        user = self.request.user
        if( user.is_organiser ):
            queryset = Lead.objects.filter( organisation = user.userprofile )
        else:
            queryset = Lead.objects.filter( organisation = user.agent.organisation )
            queryset.filter(agent__user = user)
        
        return queryset


def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request,"leads/lead_detail.html",context=context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name ="leads/create_lead.html"
    form_class= LeadModelForm

    def get_success_url(self) :
        return reverse("leads:lead-list")
    
    def form_valid(self,form):
        send_mail(
            subject="Hello",
            message="How are you doing",
            from_email="test@gmail.com",
            recipient_list=["test@gmail.com"]
        )
        return super(LeadCreateView,self).form_valid(form)
    

def create_lead(request):
    form =LeadModelForm()
    if( request.method == "POST"):
        form = LeadModelForm(request.POST);
        if(form.is_valid()):
            form.save()
            return redirect("/leads/")
    context = {
        "form": form
    }
    return render(request, "leads/create_lead.html", context=context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin,generic.UpdateView):
    template_name ="leads/lead_update.html"
    form_class= LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter( organisation = user.userprofile )

    def get_success_url(self) :
        return reverse("leads:lead-list")


def lead_update(request, pk):
    lead = Lead.objects.get(pk= pk)
    form = LeadModelForm(instance=lead)
    if(request.method == "POST"):
        form = LeadModelForm(request.POST,instance=lead)
        if(form.is_valid()):
            form.save()
            return redirect("/leads/"+str(pk)+"/details")
    context= {
        "lead":lead,
        "form":form
    }
    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin,generic.DeleteView):
    template_name = "leads/lead-delete.html"
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter( organisation = user.userprofile ) 


def lead_delete(request,pk):
    lead = Lead.objects.get(pk=pk);
    lead.delete()
    return redirect('/leads/')
