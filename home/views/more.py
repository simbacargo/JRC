from django.http import JsonResponse
from ..models import Visit
import json
import requests

def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        location = f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
        latitude, longitude = data.get("loc", "0,0").split(',')
        return location, float(latitude), float(longitude)
    except:
        return "Unknown", None, None

from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def register_visit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        ip_address = request.META.get("REMOTE_ADDR", "0.0.0.0")
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
        referrer = request.META.get("HTTP_REFERER", "")
        page_url = request.META.get("PATH_INFO", "")

        # Extracting additional device and browser details
        location, latitude, longitude = get_location(ip_address)
        device_type = "Mobile" if "Mobi" in user_agent else "Desktop"
        browser = "Unknown"
        operating_system = "Unknown"

        if "Chrome" in user_agent:
            browser = "Chrome"
        elif "Firefox" in user_agent:
            browser = "Firefox"
        elif "Safari" in user_agent and "Chrome" not in user_agent:
            browser = "Safari"
        elif "Edge" in user_agent:
            browser = "Edge"

        if "Windows" in user_agent:
            operating_system = "Windows"
        elif "Mac OS" in user_agent:
            operating_system = "macOS"
        elif "Linux" in user_agent:
            operating_system = "Linux"

        Visit.objects.create(
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type,
            browser=browser,
            operating_system=operating_system,
            location=location,
            latitude=latitude,
            longitude=longitude,
            referrer=referrer,
            page_url=page_url
        )

        return JsonResponse({"message": "Visit registered successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)
