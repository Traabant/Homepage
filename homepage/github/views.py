from django.shortcuts import render
from github.models import repos, authors

from scripts.gitHub import GitHub

# Create your views here.
def home(request):
    
    data_from_db = repos.objects.all()
    repos_list = []
    for repo in data_from_db:
        owener = authors.objects.get(git_id=repo.owner_id)
        data = {
            "id": repo.git_id,
            'name': repo.name,
            'html': repo.html,
            'git_html': repo.git_html,
            'owner': owener.login,
            'description': repo.description,
        }
        repos_list.append(data)

    
    context = {
        "repos" : repos_list
    }
    return render(request, 'github/home.html', context)
