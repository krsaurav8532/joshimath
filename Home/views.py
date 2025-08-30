from django.shortcuts import render,redirect
from .models import Event, Announcement,StotraCategory, Stotra, Carausel
from .forms import ContactForm
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse
def chunked(iterable, n):
    """Split iterable into chunks of n items"""
    return [iterable[i:i + n] for i in range(0, len(iterable), n)]

def Home(request):
    now = timezone.now()
    current_month_events = Event.objects.filter(date__year=now.year,date__month=now.month).order_by('date')[:3]  # Get only the first 3 events of the current month
    event_home = Event.objects.all()
    carausel = Carausel.objects.all().order_by('-id')[:11]  # Get the latest 5 carausel items
    # Get all announcements, order by date, and chunk them into groups of 3
    all_announcements = Announcement.objects.all().order_by('-date')
    announcement_groups = chunked(list(all_announcements), 3)


    return render(request, 'html/home.html', {
        'current_month_events': current_month_events,
        'announcement_groups': announcement_groups,
        'event_home': event_home,
        'carausel': carausel

    })


def Events(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')
    past_events = Event.objects.filter(date__lt=now).order_by('-date')
    all_events = Event.objects.all().order_by('date')

    # JSON for FullCalendar
    event_list = [
        {
            'title': event.title,
            'start': event.date.strftime("%Y-%m-%d"),
            'url': event.get_absolute_url() if hasattr(event, 'get_absolute_url') else "#",
        }
        for event in all_events
    ]

    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'all_events': all_events,
        'event_list': json.dumps(event_list, cls=DjangoJSONEncoder),
    }
    print(context['event_list'])  # Debugging line to check the JSON output

    return render(request, 'html/events.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'html/event_detail.html', {'event': event})


def Announcements(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            offset = int(request.GET.get('offset', 0))
        except (TypeError, ValueError):
            offset = 0

        limit = 10
        announcements = Announcement.objects.all().order_by('-date')[offset:offset + limit]

        data = []
        for a in announcements:
            data.append({
                'title': a.title,
                'description': a.content,
                'date': a.date.strftime('%B %d, %Y'),
                'location': a.location,
                'link': a.get_absolute_url()
            })

        return JsonResponse({'announcements': data})

    # Regular page load
    announcements = Announcement.objects.all().order_by('-date')[:10]
    return render(request, 'html/announcements.html', {
        'announcements': announcements
    })

def announcement_detail(request, slug):
    announcement = get_object_or_404(Announcement, slug=slug)
    return render(request, 'html/announcement_detail.html', {'announcement': announcement})


def Stotras(request):
    st = Stotra.objects.all().order_by('category__name', 'title')
    # Group stotras by category
    categories = {}
    for stotra in st:
        if stotra.category not in categories:
            categories[stotra.category] = []
        categories[stotra.category].append(stotra)

    # Convert to a list of tuples for easier rendering
    st = [(category, categories[category]) for category in categories]      
    # Sort categories by name
    st.sort(key=lambda x: x[0].name)    
    # Now st is a list of tuples (category, [stotras in that category])
    # Render the template with the grouped stotras
    # You can access the category name with st[0] and the stotras with st[1]
    # Example: for category, stotras in st: 
    #           print(category.name, [stotra.title for stotra in stotras])  
    # Render the template with the stotras
    
    return render(request, 'html/stotras.html', {
        'stotras': st,
    })  




def About(request):

    return render(request, 'html/about.html')   

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('Home:contact')  # Redirect to the same page to avoid form resubmission
    else:
        form = ContactForm()
    return render(request, 'html/contact.html', {'form': form})

def Services(request):
    return render(request, 'html/services.html')

def Team(request):
    return render(request, 'html/team.html')
