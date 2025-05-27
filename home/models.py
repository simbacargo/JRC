from django.db import models

class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()  # Stores browser and device info
    device_type = models.CharField(max_length=50, blank=True, null=True)  # Mobile, Desktop, Tablet
    browser = models.CharField(max_length=50, blank=True, null=True)  # Chrome, Firefox, etc.
    operating_system = models.CharField(max_length=50, blank=True, null=True)  # Windows, macOS, Linux, etc.
    screen_resolution = models.CharField(max_length=20, blank=True, null=True)  # e.g., 1920x1080
    location = models.CharField(max_length=255, blank=True, null=True)  # City, Country
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.URLField(blank=True, null=True)  # Stores where the user came from
    page_url = models.URLField(blank=True, null=True)  # Which page they visited

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"
