# python-fairdomseek

This is a VERY basic implementation of the [FAIRDOM-SEEK API](https://docs.seek4science.org/help/user-guide/api.html) in Python.

## Warnings

No tests, no guarantees 😉.

## Pre-requisites

```shell
python>=3.6,<=3.14
requests
ipykernel # optional, for Jupyter
```

## Installation

Clone the project 
```bash
git clone https://github.com/helle-ulrich-lab/python-fairdomseek
```

Install with conda

```bash
conda create -n fairdomseek_api -f requirements.conda.yml
```

Install with mamba

```bash
conda create -n fairdomseek_api -f requirements.conda.yml
```

Install with virtualenv

```bash
python3 -m venv fairdomseek_api
source fairdomseek_api/bin/activate
pip install -r requirements.pip.txt
```

## Configuration

The client is initialized with the base URL of your FAIRDOM-SEEK instance.

### Example Initialization

```python
from fairdomseek import FairdomSeek

# Initialize the client with the base URL of your FAIRDOM-SEEK instance
fairdom = FairdomSeek(
    api_base_url='https://your-fairdom-seek-instance.com',
)
```

## Authentication

The client supports both token-based authentication and username/password login. I recommend using username/password-based authentication.

### Username/Password Authentication

You can log in using your FAIRDOM-SEEK username and password (recommended):

```python
fairdom.login()  # This will prompt you for your username and password
```

### Token-Based Authentication

If you have an API token, you can alternatively authenticate with it:

```python
fairdom.login(token='your-api-token-here')
```

## Usage Examples

### Creating an Object

To create a new object of a specific type, you can use the `create` method:

```python
# Define the attributes and relationships for the new object
attributes = {
    "title": "Your title",
    "description": "Your description",
    "policy": {
        "access": "no_access",
        "permissions": [
            {"resource": {"id": "45", "type": "projects"}, "access": "manage"},
            {"resource": {"id": "1", "type": "programmes"}, "access": "view"},
        ],
    },
}

relationships = {
    "creators": {"data": [{"id": "33", "type": "people"}]},
    "projects": {"data": [{"id": "45", "type": "projects"}]},
    "studies": {
        "data": [
            {"id": "19", "type": "studies"},
        ]
    },
    "assays": {
        "data": [
            {"id": "45", "type": "assays"},
        ]
    },
}


# Create the object
response = fairdom.create(
    object_type='investigations',
    attributes=attributes,
    relationships=relationships
)

print(response)  # Output: The JSON response from the server
```

### Fetching an Object

To fetch an existing object by its ID:

```python
# Fetch an investigation with the ID '123'
response = fairdom.fetch(
    object_type='investigations',
    object_id='123'
)

print(response)  # Output: The JSON representation of the object
```

### Updating an Object

To update an existing object:

```python
# Define the updated attributes and relationships
updated_attributes = {
    'title': 'My updated title'
}

response = fairdom.update(
    object_type='investigations',
    object_id='123',
    attributes=updated_attributes,
    relationships={}
)

print(response)  # Output: The updated JSON representation of the object
```

### Deleting an Object

To delete an existing object:

```python
fairdom.delete(
    object_type='investigations',
    object_id='123'
)
# Output: "investigation 123 deleted successfully."
```

## Methods

The client provides the following methods for interacting with the FAIRDOM-SEEK API:

### `login(token='')`

Logs in the user using either a token or username/password credentials.

#### Parameters:

- `token` (str): Optional. If provided, will be used as the authentication token.

### `create(object_type, attributes, relationships)`

Creates a new object of the specified type.

#### Parameters:

- `object_type` (str): The type of object to create (e.g., "investigations").
- `attributes` (dict): A dictionary of attribute-value pairs for the object.
- `relationships` (dict): A dictionary of relationship definitions.

### `update(object_type, object_id, attributes, relationships)`

Updates an existing object.

#### Parameters:

- `object_type` (str): The type of object to update.
- `object_id` (str): The ID of the object to update.
- `attributes` (dict): A dictionary of attribute-value pairs to update.
- `relationships` (dict): A dictionary of relationship definitions to update.

### `delete(object_type, object_id)`
Deletes an existing object.

#### Parameters:

- `object_type` (str): The type of object to delete.
- `object_id` (str): The ID of the object to delete.

### `fetch(object_type, object_id)`

Fetches an existing object by its ID.

#### Parameters:

- `object_type` (str): The type of object to fetch.
- `object_id` (str): The ID of the object to fetch.
