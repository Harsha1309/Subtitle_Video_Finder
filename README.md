# Subtitle_Video_Finder

# Video Processing Website

This repository contains the code for a web application that allows users to upload videos, process them in the background, and search for specific keywords within the video subtitles. The application is built using Django and utilizes AWS services such as S3 for storing video files and DynamoDB for storing subtitles.

## Table of Contents
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/video-processing-website.git
   ```

2. Install the required dependencies. It is recommended to set up a virtual environment before installing the dependencies:

   ```bash
   cd video-processing-website
   python -m venv venv
   source venv/bin/activate  # For Unix/Linux
   # Or
   venv\Scripts\activate  # For Windows
   pip install -r requirements.txt
   ```

## Project Structure

The project has the following structure:

```plaintext
video-processing-website/
├── your_project/    # Django project directory
│   ├── your_app/    # Django app directory
│   │   ├── migrations/
│   │   ├── static/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── your_project/
│   ├── ...
│   ├── manage.py
│   └── ...
├── .gitignore
├── README.md
└── requirements.txt
```

## Usage

To use the video processing website, follow these steps:

1. Set up the necessary AWS credentials and configure your S3 bucket and DynamoDB table.
2. Configure the Django settings in `your_project/settings.py`, including the AWS credentials and S3/DynamoDB configuration.
3. Create and apply migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

5. Access the website locally by visiting `http://localhost:8000` in your web browser.

## Configuration

The configuration for the video processing website can be found in the Django project's `settings.py` file. You should update the following configurations:

- AWS credentials: Add your AWS access key and secret access key in the appropriate configuration variables.
- S3 configuration: Set the `AWS_STORAGE_BUCKET_NAME` variable to the name of your S3 bucket.
- DynamoDB configuration: Set the `DYNAMODB_TABLE_NAME` variable to the name of your DynamoDB table.

## Deployment

To deploy the video processing website to a production environment, follow these general steps:

1. Set up a production server (such as AWS EC2) and configure the necessary infrastructure.
2. Set up a production-ready web server (such as Nginx or Apache) to serve the Django application.
3. Configure the environment variables and settings for the production server.
4. Configure the DNS settings to point to the production server's IP address or domain name.

Please note that the deployment process may vary depending on your specific hosting environment and requirements.

## Contributing

Contributions to the Subtitle Video Finder website are welcome! If you find any issues or have suggestions for improvements, please feel free
