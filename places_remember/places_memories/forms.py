from django.forms import ModelForm

from places_memories.models import Memory


class MemoryForm(ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'comment']
