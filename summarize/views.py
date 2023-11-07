from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest

from .models import Submission
from .forms import sumForm
from .functions import handle_uploaded_files, query_llm

def index(request: HttpRequest) -> HttpResponse:
    """
    Generate the home page for the project

    Args:
        request (HttpRequest): the HTTP request received

    Returns:
        HttpResponse: the response given
    """
    
    query = Submission.objects.latest('date')
    summary = query.summary
    title = query.title
    show = False
    
    # if the form is submitted and valid it will be saved to the database
    if request.method == "POST":
        show = True
        form = sumForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            handle_uploaded_files(request.FILES['paper'])
            model_instance = form.save(commit=False)
            model_instance.save()   # save manually
        return redirect('result')
    
    # else a new form will be instantiated
    form = sumForm()
    
    # preparing the context to pass to the template
    context = {
        "forms": form,
        "summary": summary,
        "title": title,
        "show": show
    }
    
    return render(request, 'index.html', context)

def summary(request: HttpRequest) -> HttpResponse:
    """
    Generate the summary and populate the respected textfield

    Args:
        request (HttpRequest): the http request received

    Returns:
        HttpResponse: the response given
    """
    
    query = Submission.objects.last()
    title = query.title
    
    query.summary = query_llm()
    summary = query.summary
    query.save()
    
    form = sumForm()
    
    # preparing the context to pass to the template
    context = {
        "forms": form,
        "summary": summary,
        "title": title,
        "show": True
    }
    
    return render(request, 'index.html', context)