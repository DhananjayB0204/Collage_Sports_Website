# Sports Management Web Application

## Installation

1. Clone the repository:
   ```
   git clone git@github.com:DhananjayB0204/Collage_Sports_Department_Website.git
   
   ```
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```
   flask db upgrade
   ```
5. Run the application:
   ```
   flask run
   ```
   The application will be available at `http://localhost:5000/`.

## Usage

1. Access the application in your web browser at `http://localhost:5000/`.
2. Use the login form to authenticate as a user.
3. After logging in, you can access the following features:
   - View notices
   - Add new notices
   - Delete notices
   - Upload a banner image
   - View sports
   - Add new sports
   - Delete sports

## API

The application provides the following API endpoints:

- `GET /`: Renders the home page with the login form and notices.
- `POST /login`: Handles user login.
- `GET /logout`: Logs out the user and redirects to the home page.
- `GET /notices`: Displays the notices page with the ability to add new notices.
- `POST /delete_notice/<int:notice_id>`: Deletes a notice by the given `notice_id`.
- `GET /admin`: Renders the admin page.
- `POST /upload_banner`: Handles the upload of a banner image.
- `GET /sports_sec`: Displays the sports page with the ability to add new sports.
- `POST /delete_sport/<int:sport_id>`: Deletes a sport by the given `sport_id`.



## Testing

To run the tests, execute the following command:

```
pytest tests/
```

This will run the test suite for the application.
