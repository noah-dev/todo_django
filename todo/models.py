from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    '''Represents an item on a todo list, such as user, desc, etc.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title_text = models.CharField(max_length=200)
    desc_text = models.TextField()
    impact_text = models.TextField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    priority = models.FloatField()
    complete = models.BooleanField()
    add_date = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return self.title_text

    def __str__(self):
        return self.title_text
    def to_dict(self):
        keys = [field.name for field in self._meta.fields + self._meta.many_to_many]
        model_dict = {}
        for key in keys:
            model_dict[key]=getattr(self, key)
        return model_dict

