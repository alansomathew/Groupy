## Groupy

The Groupy is a web application that helps organizers allocate participants to rooms for events based on their preferences and room capacities. The system utilizes the maximum flow algorithm to optimize the allocation process.

This document provides an overview of the Event Management System along with detailed instructions for various functionalities.

## Table of Contents

1. [Private Event Registration](#private-event-registration)
2. [Handling Private Code Mismatch](#handling-private-code-mismatch)
3. [Event Creation](#event-creation)
4. [Dynamic Display based on Selection](#dynamic-display-based-on-selection)
5. [Generating Unique Codes](#generating-unique-codes)
6. [Adding Alphabets to Codes](#adding-alphabets-to-codes)
7. [Including Capital Letters in Codes](#including-capital-letters-in-codes)
8. [Capacity Selection for Private Events](#capacity-selection-for-private-events)
9. [Changing User Preferences](#changing-user-preferences)
10. [Pre-selecting Checkboxes](#pre-selecting-checkboxes)
11. [Retrieving User Preferences from the Database](#retrieving-user-preferences-from-the-database)
12. [Admin Changing Room Capacities](#admin-changing-room-capacities)
13. [Printing a Specific Form Section](#printing-a-specific-form-section)
14. [Printing a Form Only](#printing-a-form-only)
15. [Changing Group Capacities](#changing-group-capacities)
16. [Setting Capacity for Multiple Groups](#setting-capacity-for-multiple-groups)

---

## 1. Private Event Registration

- Users register for private events by providing a unique event code.
- Validation checks are performed to ensure the code is valid.
- Based on the event type (public/private), users are redirected accordingly.

---

## 2. Handling Private Code Mismatch

- In case of a private code mismatch, an error message is displayed to alert the user.

---

## 3. Event Creation

- Events can be created with specified details such as the number of rooms needed.

---

## 4. Dynamic Display based on Selection

- Specific input fields are displayed dynamically based on the user's selection (public/private).

---

## 5. Generating Unique Codes

- Unique 6-digit alphanumeric codes are generated for events based on the total capacity required.

---

## 6. Adding Alphabets to Codes

- The generated codes can include both numbers and alphabets (both uppercase and lowercase).

---

## 7. Including Capital Letters in Codes

- Codes can contain capital letters alongside numbers and lowercase letters.

---

## 8. Capacity Selection for Private Events

- For private events, the user needs to select the total capacity and choose between public and private options.

---

## 9. Changing User Preferences

- Users can change their preferences after submission, and this information is updated in the database.

---

## 10. Pre-selecting Checkboxes

- Previously selected groups are pre-selected for the user's convenience.

---

## 11. Retrieving User Preferences from the Database

- User preferences are stored as a list of selected groups, retrieved from the database.

---

## 12. Admin Changing Room Capacities

- Admins can change the capacities of specific groups as needed.

---

## 13. Printing a Specific Form Section

- A specific form section can be printed using JavaScript.

---

## 14. Printing a Form Only

- The form can be printed without the entire page.

---

## 15. Changing Group Capacities

- Admins can change the capacity of groups dynamically.

---

## 16. Setting Capacity for Multiple Groups

- Admins can set the capacity for multiple groups at once.

---

## Installation

1. Clone the repository to your local machine:

```
    git clone https://github.com/alansomathew/Groupy.git
```

2. Navigate to the project directory:


```
    cd Groupy
```

3. Create a virtual environment and activate it:

```
    python -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
```

4. Install the required dependencies:

``````
    pip install -r requirements.txt
``````

5. Create the database and apply migrations:

``````
    python manage.py makemigrations
    python manage.py migrate
``````

6. Run the development server:

``````
    python manage.py runserver
``````

7. Access the application in your web browser at 
``````
    http://127.0.0.1:8000/
``````

## Maximum Flow Algorithm

The maximum flow algorithm is a graph-based algorithm used in the allocation process. It is employed to optimize the allocation of participants to rooms based on their preferences and room capacities.

## Usage

1. Create an admin user to access the admin panel:
``````
    python manage.py createsuperuser
``````

2. Log in to the admin panel at http://127.0.0.1:8000/admin/ to create events, rooms, and manage participants.

3. Participants can register for events and submit their preferences through the user interface.

4. Run the allocation process by visiting the allocation page or using the management command. The system will use the maximum flow algorithm to optimize the allocation.

5. Participants' allocations, room capacities, and preferences will be displayed on the results page.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



