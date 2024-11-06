# stkpush.py
import requests
from datetime import datetime
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .genrateAcesstoken import get_access_token

@csrf_exempt
def initiate_stk_push(request):
    if request.method == 'POST':
        # Parse phone numbers from the request body
        try:
            data = json.loads(request.body)
            phone_numbers = data.get("phone_numbers", [])
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Get access token
        access_token_response = get_access_token(request)
        if isinstance(access_token_response, JsonResponse):
            access_token = access_token_response.content.decode('utf-8')
            access_token_json = json.loads(access_token)
            access_token = access_token_json.get('access_token')

            if access_token:
                # Initialize constants for STK Push
                amount = 100
                passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
                business_short_code = '174379'
                process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                callback_url = 'https://kariukijames.com/callback'
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
                account_reference = "SUBSCRIBE to Kibeezy Tv on YouTube NOW ama tukuoshe!"
                transaction_desc = 'stkpush test'
                
                stk_push_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }

                responses = []  # Store responses for each transaction
                
                # Loop through each phone number and initiate STK Push
                for phone in phone_numbers:
                    party_a = phone
                    stk_push_payload = {
                        'BusinessShortCode': business_short_code,
                        'Password': password,
                        'Timestamp': timestamp,
                        'TransactionType': 'CustomerPayBillOnline',
                        'Amount': amount,
                        'PartyA': party_a,
                        'PartyB': business_short_code,
                        'PhoneNumber': party_a,
                        'CallBackURL': callback_url,
                        'AccountReference': account_reference,
                        'TransactionDesc': transaction_desc
                    }

                    try:
                        response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                        response.raise_for_status()
                        response_data = response.json()
                        
                        # Check if STK push was successful
                        response_code = response_data.get('ResponseCode')
                        if response_code == "0":
                            responses.append({
                                'phone': phone,
                                'CheckoutRequestID': response_data['CheckoutRequestID'],
                                'ResponseCode': response_code
                            })
                        else:
                            responses.append({
                                'phone': phone,
                                'error': 'STK push failed.'
                            })
                    except requests.exceptions.RequestException as e:
                        responses.append({
                            'phone': phone,
                            'error': str(e)
                        })
                
                # Return responses for each number
                return JsonResponse({'responses': responses})
            else:
                return JsonResponse({'error': 'Access token not found.'})
        else:
            return JsonResponse({'error': 'Failed to retrieve access token.'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
