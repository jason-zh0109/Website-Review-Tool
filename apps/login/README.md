# User Authentication and Management

## Overview
This section of the application handles user authentication and management, including login, logout, signup, password reset, and email verification.

### Function Documentation

#### `login_user(request)`

- **Purpose:** Handles user login.
- **Behavior:**
  - If the request method is POST and the form is valid, it authenticates the user and logs them in.
  - Redirects to a transition page with a success message and the next URL.
  - If the form is invalid, it displays an error message.
  - If the request method is GET, it renders the login form.

#### `transition_view(request)`

- **Purpose:** Displays a transition page with a custom message and redirects to the next URL.
- **Behavior:**
  - Retrieves the next URL and a custom message from the query parameters.
  - Renders the transition page with the specified URL and message.

#### `logout_user(request)`

- **Purpose:** Logs out the user.
- **Behavior:**
  - Logs out the user and redirects to a transition page with a success message and the next URL.

#### `check_login(request)`

- **Purpose:** Checks if the user is logged in and redirects accordingly.
- **Behavior:**
  - If the user is authenticated, redirects to the search page.
  - If the user is not authenticated, redirects to the login page.

#### `index(request)`

- **Purpose:** Renders the index page.
- **Behavior:**
  - Renders the `index.html` template.

#### `reg_request_email(request, user, email)`

- **Purpose:** Sends an email to the admin for a new user registration request.
- **Behavior:**
  - Constructs an email with a registration request link.
  - Sends the email to the admin.
  - Displays a success or error message based on the email sending status.

#### `success_registration_email(request, user, email)`

- **Purpose:** Sends an email to the user informing them that their registration has been approved.
- **Behavior:**
  - Constructs an email with a success message.
  - Sends the email to the user.
  - Displays a success or error message based on the email sending status.

#### `reject_registration_email(request, user, email)`

- **Purpose:** Sends an email to the user informing them that their registration has been rejected.
- **Behavior:**
  - Constructs an email with a rejection message.
  - Sends the email to the user.
  - Displays a success or error message based on the email sending status.

#### `accept_registration(request, uidb64, token)`

- **Purpose:** Accepts a user registration request.
- **Behavior:**
  - Decodes the user ID and retrieves the user.
  - Activates the user if the token is valid.
  - Sends a success email to the user.
  - Redirects to the login page with a success message.

#### `reject_registration(request, uidb64, token)`

- **Purpose:** Rejects a user registration request.
- **Behavior:**
  - Decodes the user ID and retrieves the user.
  - Deletes the user if the token is valid.
  - Sends a rejection email to the user.
  - Redirects to the signup page with a success message.

#### `signup(request)`

- **Purpose:** Handles user signup.
- **Behavior:**
  - If the request method is POST and the form is valid, it saves the user (marked as inactive) and sends a registration request email to the admin.
  - Redirects to a transition page with a success message.
  - If the form is invalid, it displays an error message.
  - If the request method is GET, it renders the signup form.

#### `forgot_password(request)`

- **Purpose:** Handles the "forgot password" functionality.
- **Behavior:**
  - If the request method is POST and the form is valid, it sends a password reset email to the user.
  - Redirects to the index page with a success message.
  - If the form is invalid, it displays an error message.
  - If the request method is GET, it renders the forgot password form.

#### `reset_password_email(request, user, email)`

- **Purpose:** Sends a password reset email to the user.
- **Behavior:**
  - Constructs an email with a password reset link.
  - Sends the email to the user.
  - Displays a success or error message based on the email sending status.

#### `reset_password(request, uidb64, token)`

- **Purpose:** Handles the password reset functionality.
- **Behavior:**
  - Decodes the user ID and retrieves the user.
  - If the token is valid, it allows the user to reset their password.
  - Redirects to a transition page with a success message.
  - If the token is invalid, it displays an error message and redirects to the index page.