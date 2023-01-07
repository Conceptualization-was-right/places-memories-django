from django.shortcuts import render
from places_memories.forms import MemoryForm
from places_memories.models import Memory


def index(request):
    memory_form = MemoryForm()
    user_memories = Memory.objects.filter(created_by_user=request.user)
    user_memories_with_map = []
    for memory in user_memories:
        user_memory = {}
        user_memory['title'] = memory.title
        user_memory['comment'] = memory.comment
        map_url = 'https://static-maps.yandex.ru/1.x/?ll=' + str(memory.latitude) + ',' + str(memory.longitude) + '&z=8&l=map&size=200,200'
        user_memory['map_url'] = map_url
        user_memories_with_map.append(user_memory)
    if request.method == 'POST':
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        created_by_user = request.user
        memory = Memory.objects.create(title=title, comment=comment, latitude=latitude, longitude=longitude,
                                       created_by_user=created_by_user)
    return render(request, 'user_memories.html', {'form': memory_form, 'memories': user_memories_with_map})
