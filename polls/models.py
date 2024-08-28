from django.db import models
from django.utils import timezone
import datetime

# Creating question models with field question_text and date info called pub_text
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_text = models.DateTimeField('date published')

    def __str__(self): 
        return self.question_text
    
    def was_published_recently(self): # We can call this function to check if the said question was published recently
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_text <= now
    was_published_recently.admin_order_field = 'pub_date' # This will be used for admin
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

# and inside the question model we'll add the choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    

