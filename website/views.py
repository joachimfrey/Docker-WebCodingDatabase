from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import it_liste, roadmap_db, skripte_db

# Create your views here.

def index(request):
    # Statistiken
    liste_count = it_liste.objects.count()
    skripte_count = skripte_db.objects.count()
    roadmap_count = roadmap_db.objects.count()
    roadmap_done = roadmap_db.objects.filter(erledigt=True).count()
    
    # Letzte hinzugefügte Items
    latest_liste = it_liste.objects.order_by('-created_at')[:5]
    latest_skripte = skripte_db.objects.order_by('-created_at')[:5]
    latest_roadmap = roadmap_db.objects.order_by('-created_at')[:5]
    
    context = {
        'liste_count': liste_count,
        'skripte_count': skripte_count,
        'roadmap_count': roadmap_count,
        'roadmap_done': roadmap_done,
        'latest_liste': latest_liste,
        'latest_skripte': latest_skripte,
        'latest_roadmap': latest_roadmap,
    }
    return render(request, "index.html", context)


def liste(request):

    urlsystem = request.GET.get('urlsystem', '')

    if request.method == "POST":
            it_liste.objects.create(system = request.POST["system"], gruppe = request.POST["gruppe"], beschreibung = request.POST["beschreibung"], code = request.POST["code"], hinweise = request.POST["hinweise"])
            urlsystem = request.POST["system"]
    
    result_all = []

    if urlsystem:
        it_liste_system = [urlsystem]
    else:
        it_liste_system = it_liste.objects.values_list('system',flat=True).distinct()

    for system in it_liste_system:
        it_liste_gruppe = it_liste.objects.filter(system=system).values_list('gruppe',flat=True).distinct()
        subliste = []
        for gruppe in it_liste_gruppe:
            codeliste = []
            fields= ['id','created_at','system','gruppe','beschreibung','code','hinweise']
            it_liste_code = it_liste.objects.filter(system=system,gruppe=gruppe).values(*fields)
            for code in it_liste_code:
                codeliste.append(code)
            subliste.append(codeliste)
        result_all.append(subliste)
    result = result_all
    result_systems = list(it_liste.objects.values_list('system',flat=True).distinct())
    # collect distinct groups, optionally filtered by the selected system
    if urlsystem:
        result_groups = list(it_liste.objects.filter(system=urlsystem).values_list('gruppe', flat=True).distinct())
    else:
        result_groups = list(it_liste.objects.values_list('gruppe', flat=True).distinct())

    return render(request, "liste.html", {"it_liste_all":result, 'path_filter':urlsystem, 'it_liste_system':result_systems, 'it_liste_gruppe': result_groups})


def liste_edit(request):
    urlsystem = request.GET.get('urlsystem', '')
    edit_id = request.GET.get('edit','')
    
    if request.method == "POST":
        if request.POST["post_id"] == 'edit':
            member_id = request.POST["id"]
            member = it_liste.objects.get(id = member_id)
            member.system = request.POST["system"]
            member.gruppe = request.POST["gruppe"]
            member.beschreibung = request.POST["beschreibung"]
            member.code = request.POST["code"]
            member.hinweise = request.POST["hinweise"]
            member.save()
        if request.POST["post_id"] == 'delete':
            delete_id = request.POST["delete_id"]
            member = it_liste.objects.get(id=delete_id)
            member.delete()
        edit_entry = 0
    elif edit_id:
        edit_entry = it_liste.objects.get(id=edit_id)
    else:
        edit_entry = 0

    if urlsystem:
        result = it_liste.objects.filter(system=urlsystem)
    else:
        result = it_liste.objects.all()

    result_systems = list(it_liste.objects.values_list('system', flat=True).distinct())
    #if request.method == "DELETE":

    return render(request, 'liste_edit.html', {'it_liste_all':result, 'path_filter':urlsystem, 'edit_entry':edit_entry, 'it_liste_system':result_systems})


def skripte(request):
    edit_id = request.GET.get('edit', '')
    urlsystem = request.GET.get('urlsystem', '')
    edit_entry = []

    if request.method == 'POST':

        if request.POST["post_id"] == 'create':
            member = skripte_db.objects.create(system=request.POST["system"], titel="", link="", text_id="Text", text="")
            edit_id = member.id
        elif request.POST["post_id"] == 'create_entry':
            skripte_db.objects.create(system=request.POST["system"], titel=request.POST["titel"], link="", text_id="Text", text="")

        elif request.POST["post_id"] == 'edit':
            liste_id = request.POST.getlist('id')
            liste_text_id = request.POST.getlist('text_id')
            liste_link =request.POST.getlist('link')
            liste_text = request.POST.getlist('text')

            for i in range(len(liste_id)):
                member_id = liste_id[i]
                member = skripte_db.objects.get(id=member_id)
                if liste_text[i] == "":
                    if member_id == edit_id and member_id != liste_id[-1]:
                        edit_id = liste_id[i+1]
                    elif member_id == edit_id:
                        edit_id = ''
                    member.delete()
                else:
                    member.system = request.POST["system_new"]
                    member.titel = request.POST["titel_new"]
                    member.link = liste_link[i]
                    member.text_id = liste_text_id[i]
                    member.text = liste_text[i]
                    member.save()

    #skripte_db.objects.create(system = request.POST["system"],titel = request.POST["titel"],link = request.POST["link"], text_id = request.POST["text_id"], text = request.POST["text"])

    #Array erstellen um mehrere Textfelder an ein Titel zu hängen -> titel[text_id].text
    result = []
    if urlsystem:
        liste_systeme = [urlsystem]
    else:
        liste_systeme = skripte_db.objects.values_list('system',flat=True).distinct()
    if not edit_id:
        for system in liste_systeme:
            subliste = []
            skripte_titel = skripte_db.objects.filter(system=system).values_list('titel',flat=True).distinct()
            for titel in skripte_titel:
                subsubliste = []
                fields= ['id','created_at','system','titel','link','text_id','text']
                skripte_text = skripte_db.objects.filter(system=system,titel=titel).values(*fields)
                for text in skripte_text:
                    subsubliste.append(text)
                subliste.append(subsubliste)
            result.append(subliste)
    else:
        member = skripte_db.objects.get(id=edit_id)
        edit_entry = skripte_db.objects.filter(titel=member.titel).order_by('id')

    result_systems = list(skripte_db.objects.values_list('system', flat=True).distinct())

    return render(request, 'skripte.html', {'skripte':result, 'edit_entry':edit_entry, 'skripte_system':result_systems, 'path_filter':urlsystem})


def roadmap(request):
    if request.method == 'POST':
        if request.POST["post_id"] == 'create':
            roadmap_db.objects.create(ziel = request.POST["name_input"])
        if request.POST["post_id"] == 'finish':
            member_id = request.POST["finish_id"]
            member = roadmap_db.objects.get(id = member_id)
            member.erledigt = True
            member.erledigt_am = datetime.now()
            member.save()
        if request.POST["post_id"] == 'delete':
            member_id = request.POST["delete_id"]
            member = roadmap_db.objects.get(id = member_id)
            member.delete()

    result = roadmap_db.objects.all()
    return render(request, 'roadmap.html', {'roadmap':result})