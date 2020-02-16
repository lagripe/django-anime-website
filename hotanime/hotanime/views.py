from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from .model import Engine
engine = Engine()


def index(request):
    episodes = engine.get_episode_homePage(max=40)
    ongoing = engine.get_onGoing(max=30)
    return render(request, "index.html", {'episodes': episodes, 'onGoing': ongoing,'header':'Watch Anime Online Free | globalanime.com'})


def detail(request, slug):
    response = engine.check_slug(slug)
    response['info']['averageScore']/= 10
    #Converting dates
    if response['info']['start_date'] == None:
        response['info']['start_date'] = '?'
    else:
        response['info']['start_date'] = response['info']['start_date'].strftime('%b %d, %Y')
        
    if response['info']['end_date'] == None:
        response['info']['end_date'] = '?'
    else:
        response['info']['end_date'] = response['info']['end_date'].strftime('%b %d, %Y')
    # Displayed Episodes
    for episode in response['episodes']:
        try:
            episode['episodeDisplay'] = int(episode['episode'])
        except:
            episode['episodeDisplay'] = episode['episode']
        
    # GET SIMILAR ANIMES
    return render(request, "detail.html", {'info': response['info'], 'episodes': response['episodes'][::-1], 'genres': response['genres']})

def watch(request,episode):
    response = engine.get_episode_servers(episode)
    #return JsonResponse(response)
    return render(request, "watch.html",
                  {'episode': response['episode'],
                   'anime_url':response['anime_url'],
                   'last':response['last'],
                   'next':response['next'],
                   'loweredName':response['loweredName']
                   })

def anime_list(request):
    path = ''
    if request.META['PATH_INFO'].__contains__('anime-list'):
        animes = engine.get_anime_list(page=0)
        pages = engine.get_total_pages(type='animes')
        path = 'anime-list'
        header= 'Latest Anime 2020'
        
    if request.META['PATH_INFO'].__contains__('dubbed-anime'):
        animes = engine.get_dubbed_anime(page=0)
        pages = engine.get_total_pages(type='dubbed')
        path = 'dubbed-anime'
        header= 'Latest English Dubbed Anime 2020'
        
    if request.META['PATH_INFO'].__contains__('anime-series'):
        animes = engine.get_tvs(page=0)
        pages = engine.get_total_pages(type='tv')
        path = 'anime-series'
        header= 'Watch Anime Series'
        
    if request.META['PATH_INFO'].__contains__('anime-movies'):
        header= 'Watch Anime Movies'
    if request.META['PATH_INFO'].__contains__('popular'):
        animes = engine.get_popular(page=0)
        pages = engine.get_total_pages(type='popular')
        path = 'popular'
        header= 'Most Popular Animes 2020' 
    ongoing = engine.get_onGoing(max=30)
    #return JsonResponse({'animes':animes,'pages':pages})
    return render(request, "animelist.html", {'animes':animes,
                                              'totalPages':pages,
                                              'page':1,'next':2,
                                              'header':header,
                                              'onGoing':ongoing,
                                              'path':path})
def anime_list_pagination(request,page):
    try:
        page = int(page)
    except:
        pass
    if request.META['PATH_INFO'].__contains__('anime-list'):
        animes = engine.get_anime_list(page=page)
        pages = engine.get_total_pages(type='animes')
        path = 'anime-list'
        header= 'Latest Anime 2020'
    elif request.META['PATH_INFO'].__contains__('dubbed-anime'):
        animes = engine.get_dubbed_anime(page=page)
        pages = engine.get_total_pages(type='dubbed')
        path = 'dubbed-anime'
        header= 'Latest English Dubbed Anime 2020'
    elif request.META['PATH_INFO'].__contains__('anime-series'):
        animes = engine.get_tvs(page=page)
        pages = engine.get_total_pages(type='tv')
        path = 'anime-series'
        header= 'Watch Anime Series'
    elif request.META['PATH_INFO'].__contains__('anime-movies'):
        header= 'Watch Anime Movies'
        '''
    elif request.META['PATH_INFO'].__contains__('ongoing'):
        animes = engine.get_ongoing(page=page)
        pages = engine.get_total_pages(type='ongoing')
        path = 'ongoing'
        header= 'Ongoing Animes Series'
        '''
    elif request.META['PATH_INFO'].__contains__('popular'):
        animes = engine.get_popular(page=page)
        pages = engine.get_total_pages(type='popular')
        path = 'popular'
        header= 'Most Popular Animes 2020'
    
    ongoing = engine.get_onGoing(max=30)
    return render(request, "animelist.html", {'animes':animes,
                                              'pages':pages,
                                              'header':header,
                                              'page':page,'next':page+1,
                                              'totalPages':pages,
                                              'onGoing':ongoing,
                                              'path':path})

def random(request):
    anime = engine.get_random()
    # Redirection 
    return redirect("/detail/{}".format('-'.join([anime['slug'],anime['id_api']])))