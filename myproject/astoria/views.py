import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead

@csrf_exempt
def submit_lead(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')

            if not all([name, email, phone]):
                return JsonResponse({'message': 'All fields are required'}, status=400)

            # Save to local MySQL DB
            Lead.objects.create(name=name, email=email, phone=phone)

            # 🔁 Send to actual CRM API
            CRM_API_URL = "https://nirman.maksoftbox.com/MDocBoxAPI/MdocAddEnquiryORTeleCalling"
            CRM_API_KEY = "a28cc43c-526d-4010-970e-0d0e92c18902"  # Replace with actual key

            crm_response = requests.post(
                CRM_API_URL,
                json={
                    "name": name,
                    "email": email,
                    "phone": phone
                },
                headers={
                    "Authorization": f"Bearer {CRM_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=10  # Optional: prevent hanging
            )

            if crm_response.status_code == 200 or crm_response.status_code == 201:
                return JsonResponse({'message': 'Lead submitted successfully!'})
            else:
                return JsonResponse({'message': f'CRM Error: {crm_response.text}'}, status=500)

        except requests.exceptions.RequestException as e:
            return JsonResponse({'message': f'CRM Request failed: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'message': f'Server Error: {str(e)}'}, status=500)
