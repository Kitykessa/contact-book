# Contact Book

#### Video Demo: <https://youtu.be/0VjBLqwDEs0>

#### Description:

**Contact Book** is a command-line Python application that allows users to manage a collection of contacts stored in a CSV file. This project demonstrates the use of file handling, data validation, pandas for data management, and basic command-line interaction.

### Features:

* Add new contacts with name, email, and phone number
* Email and phone number validation (emails must be valid, numbers must start with '+' and contain 9–13 digits)
* Prevents duplicate entries based on name, email, or number
* Delete contacts by name with confirmation prompt
* Search contacts by name, email, or number (case-insensitive)
* Update contact information (name, email, and/or number)
* View all contacts in a formatted table
* Tests included using pytest to verify core functionalities

### File Structure:

* `project.py`: Main application file
* `test_project.py`: Contains pytest unit tests
* `contacts.csv`: CSV file that stores all contacts
* `README.md`: This file
* `requirements.txt`: List of required Python libraries

### Technologies Used:

* `pandas` for data manipulation and CSV handling
* `tabulate` for pretty-printing tables in the terminal
* `email-validator` for validating email formats
* `pytest` for unit testing

### Installation:

Make sure Python 3 is installed, then install the required packages:

```bash
pip install -r requirements.txt
```

### How to Run:

```bash
python project.py
```

### How to Test:

```bash
pytest test_project.py
```

### Sample Contact Format:

```
Name,Email,Number
John Doe,john@mail.com,+1234567890
```

### Notes:

* The video demo walks through all major features including add, search, delete, update, and load.
* The application is designed to run cross-platform (Windows, macOS, Linux) in the terminal.
* Contacts are persistently stored in `contacts.csv`.

---

Feel free to explore and improve the project!
