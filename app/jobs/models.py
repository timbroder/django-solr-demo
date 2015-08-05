from django.db import models
from localflavor.us import models as us_models

JOB_TYPES = (
    ('pt', 'Part Time'),
    ('ft', 'Full Time'),
    ('ct', 'Contract')
)

class Company(models.Model):
    name = models.CharField(max_length=64)
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField()
    
    def __unicode__(self):
        return self.name
    
class Location(models.Model):
    city = models.CharField(max_length=64)
    state = us_models.USStateField()
    
    def __unicode__(self):
        return "%s, %s" % (self.city, self.state)
    
    
class Job(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    salary = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=2, choices=JOB_TYPES)
    company = models.ForeignKey(Company, related_name='jobs')
    location = models.ForeignKey(Location, related_name='location_jobs')
    contact_email = models.EmailField(blank=True, null=True)
    added_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    def get_contact_email(self):
        if self.contact_email:
            return self.contact_email
        return self.company.contact_email
