
from django.shortcuts import render,redirect
from .models import Lead
from .forms import LeadModelForm

# Create your views here.

def landing_page(request):
    return render(request, "landing.html")


def list_leads(request):
    leads = Lead.objects.all();
    contaxt = {
        'leads': leads
    }
    return render(request,"leads/all_leads.html",context=contaxt)


def lead_detail(request,pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request,"leads/lead_detail.html",context=context)

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

def lead_delete(request,pk):
    lead = Lead.objects.get(pk=pk);
    lead.delete()
    return redirect('/leads/')