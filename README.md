
# News Data Management System

This project consists of a set of Python scripts to manage and analyze news data using MongoDB, Flask, and IBM Watson for natural language understanding.

## Setup

To run this project, you'll need Python and MongoDB installed on your system.

### Installing Python Dependencies

1. Install the required Python packages by running:
   ```
   pip install -r requirements.txt
   ```

### Setting Up MongoDB

1. Ensure MongoDB is installed and running on your system.
2. Use the provided `setup_data.py` to set up the database and collections and to load initial data.

## Running the Application

### Start the Flask Server

Run the `website/main.py` to start the Flask server:
```
python website/main.py
```

### Start the News Fetching Script

Run `server/fatch.py` to continuously fetch and update the news data:
```
python server/fatch.py
```

### Start the API for Analysis

Run `server/api.py` to start the analysis tasks using IBM Watson:
```
python server/api.py
```

## APIs

- Access the main page at `http://localhost:5001/` to view the news data.
- Use endpoints such as `/news` to interact with individual news items.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit pull requests with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
