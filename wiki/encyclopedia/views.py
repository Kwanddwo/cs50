from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(util.get_entry(title))
    })

def randompage(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[entry]))


def newpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()

        if not title:
            return render(request, "encyclopedia/newpage.html", {
                "no_title": True
            })

        if not content:
            return render(request, "encyclopedia/newpage.html", {
                "no_content": True
            })

        for entry in entries:
            if title.casefold() == entry.casefold():
                return render(request, "encyclopedia/newpage.html", {
                    "is_title_unavailable": True
                })
        
        util.save_entry(title, content)
        return HttpResponseRedirect(f"wiki/{title}")
        
    return render(request, "encyclopedia/newpage.html")


def editpage(request, cur_title):
    cur_content = util.get_entry(cur_title)

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()

        if request.POST["delete"] == "true":
            util.delete_entry(cur_title)
            return HttpResponseRedirect(reverse("index"))

        if not title:
            return render(request, "encyclopedia/newpage.html", {
                "no_title": True,
                "cur_title": cur_title,
                "cur_content": cur_content
            })

        if not content:
            return render(request, "encyclopedia/newpage.html", {
                "no_content": True,
                "cur_title": cur_title,
                "cur_content": cur_content
            })

        for entry in entries:
            if title.casefold() == entry.casefold() != cur_title.casefold():
                return render(request, "encyclopedia/editpage.html", {
                    "is_title_unavailable": True,
                    "cur_title": cur_title,
                    "cur_content": cur_content
                })
        
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/editpage.html", {
        "cur_title": cur_title,
        "cur_content": cur_content
    })


def search(request):
    if request.GET:
        query = request.GET["q"]
        entries = []

        for entry in util.list_entries():
            if query.casefold() == entry.casefold():
                return HttpResponseRedirect(reverse("entry", args=[query]))
            
            elif entry.casefold().rfind(query.casefold()) != -1:
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": entries
        })
    else:
        return HttpResponseRedirect(reverse("index"))
    
