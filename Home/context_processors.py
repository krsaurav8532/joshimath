from .models import Branches

def branches_processor(request):
    return {
        'all_branches': Branches.objects.all()
    }
