## Groupy

The Groupy is a web application that helps organizers allocate participants to rooms for events based on their preferences and room capacities. The system utilizes the maximum flow algorithm to optimize the allocation process.

## Features

- Organizers can create events and specify the number of rooms available for each event.
- Participants can submit their preferences for the rooms they want to be allocated to.
- The system uses the maximum flow algorithm to allocate participants to rooms while respecting their preferences and room capacities.
- If room capacities are exceeded or participant preferences cannot be honored, appropriate messages are displayed.
- The system allows organizers to view the allocation results and participant status.

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



