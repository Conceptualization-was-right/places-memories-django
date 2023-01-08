from django.shortcuts import render
from django.contrib.auth import logout

import folium
from places_memories.forms import MemoryForm
from places_memories.models import Memory
import requests
from jinja2 import Template

from places_remember_project.settings import VK_KEY


def index(request):
    user = request.user
    user_info = {}
    if not user.is_anonymous and 'id' in user.username:
        request_to_vk_api = 'https://api.vk.com/method/users.get?user_ids=' + str(user.username) + '&fields=photo_max&access_token=' + str(VK_KEY) + '&v=5.131'
        response = requests.get(request_to_vk_api)
        results = response.json()
        user_info['first_name'] = results['response'][0]['first_name']
        user_info['profile_picture'] = results['response'][0]['photo_max']

    return render(request, 'index.html', {'user_info': user_info})

def profile(request):
    memory_form = MemoryForm()
    user_memories = Memory.objects.filter(created_by_user=request.user)
    user_memories_with_map = []
    for memory in user_memories:
        user_memory = {}
        user_memory['title'] = memory.title
        user_memory['comment'] = memory.comment
        map_url = 'https://static-maps.yandex.ru/1.x/?l=map&pt=' + str(memory.longitude) + ',' + str(
            memory.latitude) + '&z=16&l=map&size=200,200'
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


def map(request):
    # m = folium.Map(location=[56.0141, 92.8579])
    # popup = mapper()
    # m.add_child(popup)
    # m.save('map.html')

    return render(request, 'map.html')



class mapper(folium.LatLngPopup):

    _template = Template(
        """
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                latitude = e.latlng.lat.toFixed(4);
                longitude = e.latlng.lng.toFixed(4);
                coordinates = 'data/' + latitude + "/" + longitude
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("<br /><a href="+coordinates+"> Выбрать место </a>")
                        .openOn({{this._parent.get_name()}});
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """
    )


def memories(request, latitude, longitude):
    memory_form = MemoryForm()
    if request.method == 'POST':
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        latitude = latitude
        longitude = longitude
        created_by_user = request.user
        memory = Memory.objects.create(title=title, comment=comment, latitude=latitude, longitude=longitude,
                                       created_by_user=created_by_user)
    return render(request, 'add_data.html', {'form': memory_form})


def logout_view(request):
    logout(request)

    return render(request, 'index.html')
