import requests
from django.http import JsonResponse

def get_access_token(request):
    consumer_key = "ykSVKLJEXnGo7XcrHdIp85VHEx1QPFfIDolpqOOGgNugh1xO"  
    consumer_secret = "vWAJdWV6MihnIggtfEcnrV89JfZhOJirS1AzBbQu2GancvNHdZJLN1P0YDZleG3H"  
    access_token_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    headers = {'Content-Type': 'application/json'}
    auth = (consumer_key, consumer_secret)
    try:
        response = requests.get(access_token_url, headers=headers, auth=auth)
        response.raise_for_status() 
        result = response.json()
        access_token = result['access_token']
        return JsonResponse({'access_token': access_token})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)})
    