
<div align="center">

# Gym Management System

</div>

This repository contains the source code for a Gym Management System, a web application designed to streamline gym operations. It offers features for managing memberships, trainers, schedules, and other essential aspects of gym administration.

## Table of Contents

*   [Features](#features)
*   [Installation](#installation)
*   [Running the Project](#running-the-project)
*   [Dependencies](#dependencies)
*   [Contributing](#contributing)
-
## Features

*   **Membership Management:** Tools for managing member profiles, subscription plans, and payment history.
*   **Trainer Management:** Features to add, update, and manage trainer information, including schedules and specializations.
*   **Scheduling:** Functionality for creating and managing class schedules and appointments.
*   **Reporting:** Generate reports on key metrics, such as membership statistics and revenue.
*   **User Authentication:** Secure login and registration for members and staff.
*   **Content Management:** Manage banners, services offered, FAQs, and gallery images.
*   **Enquiry System:** Handle customer enquiries and details.
*   **Subscription Plans:** Manage subscription plans, features, and discounts.
*   **Notifications:** Implement user and trainer notification system.

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/mayurexh/Gym-Management-System-Latest.git
    cd Gym-Management-System-Latest
    ```

2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Apply migrations:

    ```bash
    python manage.py migrate
    ```

## Running the Project

1.  Start the development server:

    ```bash
    python manage.py runserver
    ```

2.  Access the application in your web browser at `http://localhost:8000`.

## Dependencies

*   Django
*   django-bootstrap5
*   Pillow
*   Other dependencies specified in `requirements.txt`

## Contributing

Contributions are welcome! To contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Submit a pull request.

