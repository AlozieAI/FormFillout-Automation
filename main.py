from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

app = Flask(__name__)


@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Extract parameters from the incoming request
    data = request.get_json()
    custom_812 = data.get('custom_812',
                          'Test')  # Default to 'Test' if not provided
    contact_prefix = data.get('contact_prefix', '4')  # Default to '3' (M.)
    contact_first_name = data.get('contact_first_name')
    contact_last_name = data.get('contact_last_name')
    contact_phone = data.get('contact_phone')
    contact_email = data.get('contact_email')

    # Validate required parameters
    required_fields = [
        'contact_first_name', 'contact_last_name', 'contact_phone',
        'contact_email'
    ]
    missing_fields = [
        field for field in required_fields if data.get(field) is None
    ]
    if missing_fields:
        return jsonify({
            'status':
            'error',
            'message':
            f'Missing required fields: {", ".join(missing_fields)}'
        }), 400

    try:
        # Create a session to persist cookies and session info
        session = requests.Session()

        # Step 1: GET the form page to extract dynamic tokens and form_build_id
        form_page_url = "https://lacliniquefinanciere.com/fr/form/demande-de-service"
        response = session.get(form_page_url)
        response.raise_for_status()  # Check for HTTP errors

        # Record the time when the form was loaded
        form_load_time = datetime.now()

        # Parse the HTML page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the form_build_id, honeypot_time, and form_id from the form
        form_build_id = soup.find('input', {'name': 'form_build_id'})['value']
        honeypot_time = soup.find('input', {'name': 'honeypot_time'})['value']
        form_id = soup.find('input', {'name': 'form_id'})['value']

        # Step 2: Prepare the payload with the extracted form_build_id and other required fields
        payload = {
            'description_de_la_demande': custom_812,
            'nom[first]': contact_first_name,
            'nom[last]': contact_last_name,
            'civicrm_1_contact_1_phone_phone': contact_phone,
            'telephone': contact_email,
            'form_build_id': form_build_id,
            'form_id': form_id,
            'honeypot_time': honeypot_time,  # We'll adjust this value below
            'op': 'Submit',  # Correct submit button value
            'url': ''  # Leave the anti-bot field empty
        }

        # Step 3: Introduce a 6-second delay before submitting the form
        time.sleep(6)  # Wait for 6 seconds

        # Update the honeypot_time to reflect the time elapsed
        time_elapsed = int((datetime.now() - form_load_time).total_seconds())
        payload['honeypot_time'] = str(time_elapsed)

        # Step 4: POST the form data to submit the form
        post_url = "https://lacliniquefinanciere.com/fr/form/demande-de-service"
        headers = {
            'User-Agent': 'Mozilla/5.0',  # Mimic a real browser request
            'Referer': form_page_url,
            'Origin': 'https://lacliniquefinanciere.com'
        }

        # Perform the POST request with the session to maintain cookies
        response = session.post(post_url, data=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        # Check if the form submission was successful
        if "Nouvelle soumission ajoutée à Demande de service" in response.text:
            return jsonify({
                'status': 'success',
                'message': 'Form submitted successfully!'
            }), 200
        else:
            # For debugging, you can extract error messages from the response
            soup = BeautifulSoup(response.text, 'html.parser')
            error_message = soup.find('div', {'role': 'alert'})
            error_text = error_message.get_text(
                strip=True) if error_message else 'Unknown error'
            return jsonify({
                'status':
                'error',
                'message':
                f'There was an error submitting the form: {error_text}'
            }), 400

    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({
            'status': 'error',
            'message': f'An exception occurred: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
