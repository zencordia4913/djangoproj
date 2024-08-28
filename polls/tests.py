import datetime


from django.test import TestCase
from django.utils import timezone


# Create your tests here.

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_text = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than one than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_text=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True from questions whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(hours = 23, minutes=59, seconds=59)
        recent_question = Question(pub_text=time)
        self.assertIs(recent_question.was_published_recently(), True)

from django.urls import reverse

def create_question(question_text, days):
    """
    Create a question with given 'question_text' and published the given number of days offset to now
    (negative for questions published in the past, positive for question that have yet to be published)
    """
    time = timezone.now() + timezone.timedelta(days = days)
    return Question.objects.create(question_text=question_text, pub_text=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed in the index page.
        """
        pastquestion = create_question(question_text="Past Question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [pastquestion]
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on the index page
        """
        create_question(question_text="Future Question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_questions_and_past_questions(self):
        """
        Even if both past and future questions exist, only past questions are displayed
        """
        pastquestion = create_question(question_text="Past Question.", days=-30)
        futurequestion = create_question(question_text="Future Question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [pastquestion]
        )
    
    def test_two_past_questions(self):
        """
        The question index page may display multiple questions.
        """
        question1 = create_question(question_text = "Past Question 1.", days=-30)
        question2 = create_question(question_text = "Past Question 2.", days=-5)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            [question2,question1] 
        )

class QuestionDetailsViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found
        """
        future_question = create_question(question_text='Future Question.', days=5)
        url = reverse('polls:details', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse('polls:details', args=(past_question.id,))
        response = self.client.get(url) 

        self.assertContains(response, past_question)     