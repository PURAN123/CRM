from django.shortcuts import reverse
from django.views import generic
from leads.models import Agent
from .mixins import OrganizerAndLoginRequiredMixin
from .forms import AgentModelForm
from django.core.mail import send_mail

# Create your views here.

class AgentListView(OrganizerAndLoginRequiredMixin,generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_organiser = False
        user.is_agent=True
        user.set_password("random")
        user.save()
        Agent.objects.create(
            user=user,
            organisation = self.request.user.userprofile
        )
        send_mail(
            subject="Invitation for Agent",
            message=f"Hello {user.username},\nTou are invited for agent.",
            from_email="admin@gmail.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
    

class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.all()


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"


    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)





