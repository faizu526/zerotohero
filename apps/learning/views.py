from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import HiddenGem, Roadmap, RoadmapPhase, Certification, Lab, GemCategory

def hidden_gems(request):
    """Hidden Gems Page - 200+ Secret Resources"""
    gems = HiddenGem.objects.filter(is_active=True)
    
    # Category filter
    category = request.GET.get('category')
    if category:
        gems = gems.filter(category__slug=category)
    
    # Search
    q = request.GET.get('q')
    if q:
        gems = gems.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(provider__icontains=q)
        )
    
    # Featured
    featured = gems.filter(is_featured=True)[:4]
    
    context = {
        'gems': gems,
        'categories': GemCategory.objects.all(),
        'featured': featured,
        'total_count': gems.count(),
    }
    return render(request, 'learning/hidden-gems.html', context)

def hidden_gem_detail(request, slug):
    """Single Hidden Gem Detail"""
    gem = get_object_or_404(HiddenGem, slug=slug, is_active=True)
    gem.views += 1
    gem.save()
    return render(request, 'learning/hidden-gem-detail.html', {'gem': gem})

def roadmap(request):
    """Learning Roadmaps Page"""
    roadmaps = Roadmap.objects.filter(is_active=True)
    
    # Featured
    featured = roadmaps.filter(is_featured=True)[:3]
    
    context = {
        'roadmaps': roadmaps,
        'featured': featured,
    }
    return render(request, 'learning/roadmap.html', context)

def roadmap_single(request, slug):
    """Single Roadmap Detail"""
    roadmap = get_object_or_404(Roadmap, slug=slug, is_active=True)
    phases = roadmap.phases.all()
    
    context = {
        'roadmap': roadmap,
        'phases': phases,
    }
    return render(request, 'learning/roadmap-single.html', context)

def certifications(request):
    """Certifications Page"""
    certs = Certification.objects.filter(is_active=True)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        certs = certs.filter(difficulty=difficulty)
    
    # Filter by price type
    price_type = request.GET.get('price_type')
    if price_type:
        certs = certs.filter(price_type=price_type)
    
    # Featured
    featured = certs.filter(is_featured=True)[:4]
    
    context = {
        'certs': certs,
        'featured': featured,
    }
    return render(request, 'learning/certifications.html', context)

def labs(request):
    """Practice Labs Page"""
    labs_list = Lab.objects.filter(is_active=True)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        labs_list = labs_list.filter(category=category)
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        labs_list = labs_list.filter(difficulty=difficulty)
    
    # Free filter
    if request.GET.get('free') == 'true':
        labs_list = labs_list.filter(is_free=True)
    
    # Featured
    featured = labs_list.filter(is_featured=True)[:4]
    
    context = {
        'labs': labs_list,
        'featured': featured,
    }
    return render(request, 'learning/labs.html', context)

