# FormFillout-Automation

This project is a web automation tool built in Python using Flask to automate the process of filling out and submitting service request forms for customers during a phone call. The automation script is designed to be triggered through function calls within VAPI, which powers an AI Phone Agent, ensuring efficient and accurate form submissions.

**Features**

Automated Form Submission: Automatically fills out and submits a service request form on behalf of customers.

Dynamic Token Extraction: Extracts and uses tokens such as form_build_id and honeypot_time to successfully submit the form.

Session Persistence: Maintains cookies and session data for a more reliable interaction with the target website.

Error Handling: Provides meaningful error messages and status codes in case of issues during the form submission process.

Request Validation: Checks for missing required fields and returns appropriate error messages.

**How It Works**

Receive Data: The API receives a JSON payload with customer information (e.g., name, phone number, email) from the VAPI AI Phone Agent.

Fetch Form Tokens: The script performs a GET request to the form page to extract required tokens like form_build_id and honeypot_time using BeautifulSoup.

Prepare Payload: Constructs the form submission payload with the extracted tokens and customer data.

Delay for Honeypot: Introduces a 6-second delay to simulate human interaction, updating the honeypot_time accordingly.

Submit Form: Uses a POST request to submit the form data, mimicking a real browser request with appropriate headers.

Handle Response: Checks for a success message in the response and returns a status indicating whether the form submission was successful or not.

**Setup and Installation**

Prerequisites

Python 3.8+

Flask: A lightweight WSGI web framework for Python.

Requests: A simple HTTP library for Python.

BeautifulSoup: A library for parsing HTML and XML documents.

Installation Steps
Clone the Repository

bash

```
git clone <repository-url>
cd <repository-folder>
```

Install Dependencies

bash

```
pip install Flask requests beautifulsoup4
```

Run the Application

bash

```
python app.py
```

The API will be available at http://0.0.0.0:8080.

**API Endpoint**

POST /submit-form

Description: Automates the form submission process using the provided customer details.

Request Body: JSON format with the following fields:

custom_812: (Optional) Description of the service request. Defaults to 'Test'.

contact_prefix: (Optional) Prefix for the contact. Defaults to '4'.

contact_first_name: (Required) First name of the contact.

contact_last_name: (Required) Last name of the contact.

contact_phone: (Required) Phone number of the contact.

contact_email: (Required) Email of the contact.

Response: JSON response with status and message.

Example Request

json
```
{
  "custom_812": "Service request description",
  "contact_prefix": "4",
  "contact_first_name": "John",
  "contact_last_name": "Doe",
  "contact_phone": "1234567890",
  "contact_email": "john.doe@example.com"
}
```

Example Response

Success:

json
```

{
  "status": "success",
  "message": "Form submitted successfully!"
}
```

Error:

json 

```
{
  "status": "error",
  "message": "There was an error submitting the form: Unknown error"
}
```

**How to Use**

Send a POST request to /submit-form with the necessary customer information in the request body.

Validate the response to ensure the form submission was successful or to handle errors accordingly.

**Notes**

Session Management: The script uses a requests.Session object to persist cookies and session data.

Delay for Honeypot: A 6-second delay is added to comply with the website's anti-bot measures.

Error Handling: Detailed error messages are returned in case of missing fields, HTTP errors, or exceptions.

Troubleshooting

Missing Fields: Ensure all required fields (contact_first_name, contact_last_name, contact_phone, contact_email) are provided in the request.

HTTP Errors: Check the website URL and ensure it is reachable. Verify if there are changes to the form structure on the target website.

Debugging: Use the logged error messages and the response content for debugging issues with form submission.
