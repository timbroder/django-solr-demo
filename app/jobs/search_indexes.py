import datetime
from haystack import indexes
from .models import Job

class JobIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    type = indexes.CharField(model_attr='type', faceted=True)
    location = indexes.CharField(model_attr='location', faceted=True)
                             
    def get_model(self):
        return Job
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
