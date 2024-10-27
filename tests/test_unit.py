from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import requests
from bs4 import BeautifulSoup
# Log In Tests
class UserLogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    # valid username and password
    def test_valid_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
    # Existing username & unmatched password
    def test_login_incorrect_username(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'validpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password.')

    # Non-existing username & arbitrary password
    def test_login_incorrect_password(self):
        response = self.client.post(reverse('login'), {
            'username': 'validuser',
            'password': 'invalidpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password.')

# Sign Up Tests
class UserSignUpTest(TestCase):
    # ensure signup page is accessible
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    # Valid username, valid email address and matched passwords
    def test_signup_valid_form(self):
        response = self.client.post(reverse('signup'), {
            'username': 'validsignupuser',
            'email': 'validemail@gmail.com',
            'password1': 'val1dpassw0rd',
            'password2': 'val1dpassw0rd'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('transition') + '?next=/login/&message=Register+Successful%21')
    def test_signup_invalid_username(self):
        response = self.client.post(reverse('signup'), {
            'username': 'te',
            'email': 'validemail@example.com',
            'password1': 'val1dpassw0rd',
            'password2': 'val1dpassw0rd',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFormError(response, 'form', 'username', 'Username must be 5-20 characters long and can only contain letters, numbers, and underscores')


    # Existing username
    def test_signup_existing_username(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'validemail@example.com',
            'password1': 'val1dpassw0rd',
            'password2': 'val1dpassw0rd',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

    # password is too simple
    def test_signup_simple_password(self):
        response = self.client.post(reverse('signup'), {
            'username': 'validuser',
            'email': 'validemail@gmail.com',
            'password1': 'asdfghjk',
            'password2': 'asdfghjk',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFormError(response, 'form', 'password2', 'This password is too common.')
    def test_signup_short_password(self):
        response = self.client.post(reverse('signup'), {
            'username': 'validuser',
            'email': 'validemail@gmail.com',
            'password1': 'adsioj',
            'password2': 'adsioj',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFormError(response, 'form', 'password2', 'This password is too short. It must contain at least 8 characters.')

    # passwords do not match
    def test_signup_mismatch_password(self):
        response = self.client.post(reverse('signup'), {
            'username': 'validuser',
            'email': 'validemail@gmail.com',
            'password1': 'pa55w0rd1',
            'password2': 'pa55w0rd2',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
    # numeric password
#     def test_numeric_password(self):
        response = self.client.post(reverse('signup'), {
            'username': 'validuser',
            'email': 'validemail@gmail.com',
            'password1': '2815481828',
            'password2': '2815481828',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'This password is entirely numeric.')
    def test_signup_invalid_email(self):
        response = self.client.post(reverse('signup'), {
            'username': 'validsignupuser',
            'email': 'validemail@',
            'password1': 'val1dpassw0rd',
            'password2': 'val1dpassw0rd'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

#
#
# Forgot Password Tests
class UserForgotPasswordTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret',
            'email': 'nonexistent@example.com'
        }
        User.objects.create_user(**self.credentials)
    def test_forgot_password_view(self):
        response = self.client.get(reverse('forgot_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forgot_password.html')

    def test_forgot_password_wrong_email(self):
        response = self.client.post(reverse('forgot_password'), {
            'username':'testuser',
            'email': 'nonexisten@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No account found with the provided username and email.')
        self.assertTemplateUsed(response, 'forgot_password.html')
        self.assertEqual(len(mail.outbox), 0)
    def test_forgot_password_non_exising_user(self):
        response = self.client.post(reverse('forgot_password'), {
            'username':'testus',
            'email': 'nonexisten@example.com',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No account found with the provided username and email.')
        self.assertTemplateUsed(response, 'forgot_password.html')
        self.assertEqual(len(mail.outbox), 0)




class SearchLinkTestCase(TestCase):
    def setUp(self):
        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_broken_link_result(self):
        # Step 1: Get the search_link page
        response = self.client.get(reverse('search_link'))
        self.assertEqual(response.status_code, 200)

        # Step 2: Post data to the search_link view
        response = self.client.post(reverse('search_link'), {
            'url': 'https://sites.research.unimelb.edu.au/research-funding/nhmrc',

        })
        self.assertEqual(response.status_code, 302)  # Check for redirect to show_results

        # Optional: Wait if the processing takes time
        # time.sleep(40)  # Adjust sleep time as needed

        # Step 3: Get the show_results page
        response = self.client.get(reverse('show_results'))
        self.assertEqual(response.status_code, 200)

        # Step 4: Check if the session data has been correctly passed to the template
        self.assertIn('results', response.context)  # Ensure 'results' exists in context
        self.assertIn('show_source_link', response.context)  # Check for 'show_source_link' presence
        self.assertIn('token', response.context)  # Check for 'token' presence

        # Step 5: Verify the content of 'results' and 'show_source_link'
        results = response.context['results']
        for result in results:
            self.assertEquals(requests.get(result['url']).status_code, 404)
            temp_response = requests.get(result['source_link'])
            soup = BeautifulSoup(temp_response.text, 'html.parser')
            target_href = result['url']
            associated_text = soup.find('a', href=target_href).get_text()
            self.assertEquals(associated_text, result['associated_text'])

        show_source_link = response.context['show_source_link']
        token = response.context['token']

        # Adjust these assertions based on expected results
        self.assertIsNotNone(results)  # Make sure results are not None
        self.assertIsInstance(results, list)  # Assume results are a list (update as needed)
        self.assertTrue(show_source_link is True or show_source_link is False)  # Boolean check
        self.assertIsNotNone(token)  # Ensure token is set
    def test_keyword_result(self):
        # Step 1: Get the search_link page
        response = self.client.get(reverse('search_link'))
        self.assertEqual(response.status_code, 200)

        # Step 2: Post data to the search_link view
        response = self.client.post(reverse('search_link'), {
            'url': 'https://sites.research.unimelb.edu.au/research-funding/nhmrc',
            'specifiedText': 'Accepting and managing your funding'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect to show_results

        # Optional: Wait if the processing takes time
        # time.sleep(40)  # Adjust sleep time as needed

        # Step 3: Get the show_results page
        response = self.client.get(reverse('show_results'))
        self.assertEqual(response.status_code, 200)

        # Step 4: Check if the session data has been correctly passed to the template
        self.assertIn('results', response.context)  # Ensure 'results' exists in context
        self.assertIn('show_source_link', response.context)  # Check for 'show_source_link' presence
        self.assertIn('token', response.context)  # Check for 'token' presence

        # Step 5: Verify the content of 'results' and 'show_source_link'
        results = response.context['results']
        for result in results:

            self.assertEquals(requests.get(result['url']).status_code, 200)
            temp_response = requests.get(result['url'])
            soup = BeautifulSoup(temp_response.content, 'html.parser')
            keyword_list = result['associated_text'].split()
            text_content = soup.get_text()
            self.assertTrue(any(keyword in text_content for keyword in keyword_list),
                            "None of the keywords were found in the text.")

        show_source_link = response.context['show_source_link']
        token = response.context['token']

        # Adjust these assertions based on expected results
        self.assertIsNotNone(results)  # Make sure results are not None
        self.assertIsInstance(results, list)  # Assume results are a list (update as needed)
        self.assertTrue(show_source_link is True or show_source_link is False)  # Boolean check
        self.assertIsNotNone(token)  # Ensure token is set
