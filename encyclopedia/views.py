from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.utils.html import format_html
import random
import re
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_title):
    entry = util.get_entry(entry_title)
    if entry:
        content = format_html(markdown2.markdown(entry))
        return render(request, "encyclopedia/entry.html", {'title': entry_title, 'content': content})
    return HttpResponseNotFound(f"'{entry_title}' Entry doesn't exist.")

def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        entry = util.get_entry(query)
        if entry:
            return HttpResponseRedirect(reverse("entry", args=[entry]))
        entries = util.list_entries()
        rex = re.compile(query, re.IGNORECASE)
        results = filter(rex.search, entries)        
    return render(request, "encyclopedia/results.html", {"results": results, "query": query})

def new_entry(request):
    if request.method == "POST":
        title = request.POST["title"]
        if util.get_entry(title):
            message = f"Entry with title '{title}' already exist!"
            return render(request, "encyclopedia/new_entry.html", {"message": message})
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/new_entry.html")

def edit_entry(request, entry_title):
    if request.method == "POST":
        new_content = request.POST["content"]
        util.save_entry(entry_title, new_content)
        context = {
            "title": entry_title,
            "content": new_content,
            "edit": False
        }
        # return render(request, "encyclopedia/entry.html", context=context)
        return HttpResponseRedirect(reverse("entry", args=[entry_title]))
    content = util.get_entry(entry_title)
    context = {
        "title": entry_title,
        "content": content,
        "edit": True
    }
    return render(request, "encyclopedia/entry.html", context=context)

def random_entry(request):
    choices = util.list_entries()
    title = random.choice(choices)
    return HttpResponseRedirect(reverse("entry", args=[title]))

