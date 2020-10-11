from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
from markdown2 import Markdown
from django import forms

class NewWikiForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Content")

class WikiEditForm(forms.Form):
    title = forms.CharField(strip=True)
    content = forms.CharField(widget=forms.Textarea(), label=False, strip=True)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, page):
    markdowner = Markdown()
    pageContent = util.get_entry(page)
    if pageContent:
        return render(request, "encyclopedia/pages.html", {
            "pageName": page,
            "pageContent": markdowner.convert(pageContent)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "pageName": page
        })

def search(request):
    searchTerm = request.GET.get("q")
    pageList = util.list_entries()
    markdowner = Markdown()
    match = []
    if searchTerm in pageList:
        pageContent = util.get_entry(searchTerm)
        return render(request, "encyclopedia/pages.html", {
            "pageName": searchTerm,
            "pageContent": markdowner.convert(pageContent)
        })
    else:
        for page in pageList:
            if searchTerm in page:
                match.append(page)
                
        return render(request, "encyclopedia/index.html", {
            "search": True,
            "searchTerm": searchTerm,
            "entries": match
        })

def newpage(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/newpage.html", {
                    "exists": True,
                    "title": title,
                    "form": form
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:page", kwargs={"page": title}))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form":form,
                "notValid":True
            })
    return render(request, "encyclopedia/newpage.html",{
        "form": NewWikiForm()
    })

def edit(request, page):
    if request.method == "POST":
        newForm = WikiEditForm(request.POST)
        if newForm.is_valid():
            title = newForm.cleaned_data["title"]
            content = newForm.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:page", kwargs={"page":page}))
    else:
        form = WikiEditForm()
        form.fields["title"].initial = page
        form.fields["title"].widget = forms.HiddenInput()
        pageContent = util.get_entry(page)
        form.fields["content"].initial = pageContent
        return render(request, "encyclopedia/edit.html", {
            "pageTitle": page,
            "pageContent": pageContent,
            "form": form
        })