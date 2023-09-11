# Flask OAuth 2.0 Membership Platform

The Flask OAuth 2.0 Membership Platform is a web application designed to provide membership management capabilities with OAuth 2.0 authentication. It includes features for user accounts, payments, and administration. This README provides an overview of the project and instructions for setting it up.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [OAuth 2.0 Integration](#oauth-20-integration)
- [Admin Dashboard](#admin-dashboard)
- [License](#license)

## Features

- User account management.
- OAuth 2.0 authentication integration.
- Payment processing capabilities.
- Admin dashboard for managing users and payments.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher installed.
- SQLAlchemy and Flask-SQLAlchemy.
- Flask and other required dependencies (install using `pip install -r requirements.txt`).
- OAuth 2.0 credentials from your chosen OAuth provider.
- Configuration settings (see [Configuration](#configuration)).

## Getting Started

1. Clone this repository:

   ```shell
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:

   ```shell
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up your configuration settings (see [Configuration](#configuration)).

5. Run the application:

   ```shell
   flask run
   ```

The application will start, and you can access it locally in your web browser.

## Project Structure

The project structure is organized as follows:

- `app`: This directory contains the main application code.
  - `__init__.py`: Initializes the Flask application.
  - `main`: The main application blueprint.
  - `account`: Blueprint for managing user accounts.
  - `oauth`: Blueprint for OAuth 2.0 integration.
  - `payment`: Blueprint for handling payment processing.
  - `webhook`: Blueprint for handling webhooks.
  - `admin`: Blueprint for the admin dashboard.
  - `static`: This directory is used for storing static assets like CSS, JavaScript, and images.
  - `templates`: Contains HTML templates used by the application.
- `config.py`: The configuration file where you define application settings, such as database configurations and OAuth 2.0 credentials.
- `run.py`: A script to start the Flask development server.
- `app.py`: The main application entry point.
- `requirements.txt`: Lists all project dependencies. You can install these dependencies using `pip install -r requirements.txt`.
- `zappa_settings.json`: Configuration file for deploying the application with Zappa, if applicable.


## Configuration

The application's configuration settings can be found in the `config.py` file. You must configure the following settings:

- OAuth 2.0 credentials (client ID and client secret).
- Database configuration (e.g., database URL).
- Other application-specific settings.

## Usage

The application provides several features accessible via different endpoints. Refer to the [Usage](#usage) section in the project's documentation for detailed information on using these features.

## OAuth 2.0 Integration

OAuth 2.0 authentication is integrated into the platform. You need to configure OAuth 2.0 credentials from your chosen OAuth provider and set them in the `config.py` file.

## Admin Dashboard

The project includes an admin dashboard accessible at the `/sfadmin` URL. This dashboard allows you to manage users, payments, and other administrative tasks.

## License

This project is licensed under the GNU General Public License, version 2 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Stripe](https://stripe.com/docs/api)
