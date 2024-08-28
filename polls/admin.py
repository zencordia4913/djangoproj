from django.contrib import admin

# Register your models here.
from .models import Question
from .models import Choice, Question

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_text'], 'classes': ['collapse']}),
    ] # Custom look for the admin
    inlines = [ChoiceInLine] # This allows us to add/edit choices within the question
    list_display = ('question_text', 'pub_text', 'was_published_recently') # Things to display in admin
    list_filter = ['pub_text'] # We can filter by date
    search_fields = ['question_text'] # We can filter by a search field above

admin.site.register(Question, QuestionAdmin)