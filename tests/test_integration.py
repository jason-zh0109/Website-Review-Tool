# from django.contrib.auth.models import User
# from django.test import LiveServerTestCase
# from django.urls import reverse
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# import time
#
#
# class CopyLinkAfterLoginTest(LiveServerTestCase):
#     def setUp(self):
#         # Create a test user
#         self.username = 'testuser'
#         self.password = 'testpassword'
#         self.user = User.objects.create_user(username=self.username, password=self.password)
#
#         # Set up Selenium WebDriver
#         self.driver = webdriver.Chrome()  # or use webdriver.Firefox() for Firefox
#         self.driver.implicitly_wait(10)  # Wait for elements to load
#
#     def tearDown(self):
#         # Close the browser after each test
#         self.driver.quit()
#
#     def login(self):
#         # Go to the login page
#         login_url = self.live_server_url + reverse('login')  # Replace 'login' with your actual login URL name
#         self.driver.get(login_url)
#
#         # Enter username and password
#         self.driver.find_element(By.ID, "username").send_keys(self.username)
#         self.driver.find_element(By.ID, "password").send_keys(self.password)
#
#         # Submit the login form
#         login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
#         login_button.click()
#
#     def test_copy_link_to_clipboard_after_login(self):
#         # Step 1: Log in
#         self.login()
#
#         # Step 2: Navigate to the search results page after login
#         url = self.live_server_url + reverse('show_results')  # Replace with your actual view name
#         self.driver.get(url)
#
#         # Step 3: Find the "Copy Link" button and click it
#         copy_button = self.driver.find_element(By.XPATH, "//button[@onclick=\"copyToClipboard('link1')\"]")
#         copy_button.click()
#
#         # Step 4: Wait for the clipboard to be updated
#         time.sleep(1)  # Adjust as needed
#
#         # Step 5: Open a temporary input element and paste the clipboard contents
#         actions = ActionChains(self.driver)
#         actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
#
#         # Step 6: Retrieve the copied URL from the href of the link
#         link_element = self.driver.find_element(By.ID, "link1")
#         link_url = link_element.get_attribute("href")
#
#         # Step 7: Verify if clipboard content matches the expected URL
#         pasted_content = self.driver.find_element(By.TAG_NAME, "body").text
#         self.assertEqual(pasted_content, link_url)
#
#         print("Test passed: Link copied to clipboard successfully after login")
