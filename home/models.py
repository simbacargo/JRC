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


from .utils import format_text

class WelcomeMessage(models.Model):
    message = models.TextField(blank=True, null=True, help_text="Detailed description of the event")
    
    def save(self, *args, **kwargs):
        if self.message:
            self.message = format_text(self.message)
        super().save(*args, **kwargs)




from django.db import models
from django.utils import timezone
from django.urls import reverse # Used for get_absolute_url
import os # For clean_image_path method

class Event(models.Model):
    """
    Model to represent a church event with enhanced fields and methods.
    """
    # Core Event Details (title and description were already present)
    title = models.CharField(max_length=200, help_text="Title of the event (e.g., 'Sunday Service', 'Youth Retreat')")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the event")

    # New Fields for Images
    image = models.ImageField(
        upload_to='event_images/', # Files will be saved in MEDIA_ROOT/event_images/
        blank=True,
        null=True,
        help_text="Upload an image for the event poster or banner."
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Alternative text for the event image, crucial for accessibility."
    )

    # Date and Time Fields (Using DateTimeField for robustness)
    start_time = models.DateTimeField(help_text="The date and time the event is scheduled to start.")
    end_time = models.DateTimeField(blank=True, null=True, help_text="The date and time the event is scheduled to end (optional).")

    # Existing Fields
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Physical location or online link for the event.")
    event_type = models.CharField(
        max_length=50,
        choices=[
            ('service', 'Regular Service'),
            ('special', 'Special Event'),
            ('youth', 'Youth Gathering'),
            ('children', 'Children\'s Program'),
            ('meeting', 'Meeting'),
            ('other', 'Other'),
        ],
        default='service',
        help_text="Category of the event."
    )
    is_published = models.BooleanField(default=False, help_text="Whether the event is publicly visible.")
    registration_required = models.BooleanField(default=False, help_text="Indicates if attendees need to register.")
    registration_deadline = models.DateTimeField(blank=True, null=True, help_text="Last date/time for registration.")
    max_attendees = models.IntegerField(blank=True, null=True, help_text="Maximum number of attendees allowed.")
    contact_person = models.CharField(max_length=100, blank=True, null=True, help_text="Name or department for event inquiries.")
    contact_email = models.EmailField(blank=True, null=True, help_text="Email for event inquiries.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time'] # Default ordering for events
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        # Format the display string for clarity
        start_date_str = self.start_time.strftime('%b %d, %Y')
        start_time_str = self.start_time.strftime('%I:%M %p')
        return f"{self.title} on {start_date_str} at {start_time_str}"

    # --- Properties for extracting Date and Time ---
    @property
    def event_date(self):
        """Returns just the date part of the start_time."""
        return self.start_time.date()

    @property
    def event_time(self):
        """Returns just the time part of the start_time."""
        return self.start_time.time()

    # --- New Methods ---
    def get_absolute_url(self):
        """
        Returns the URL to access a particular event instance.
        You'll need to define a URL pattern in your app's urls.py
        like path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail')
        """
        return reverse('event_detail', args=[str(self.id)])

    def is_upcoming(self):
        """Checks if the event is in the future."""
        return self.start_time > timezone.now() and self.is_published

    def has_started(self):
        """Checks if the event's start time has passed."""
        return self.start_time <= timezone.now()

    def has_ended(self):
        """Checks if the event's end time has passed (if an end time exists)."""
        if self.end_time:
            return self.end_time <= timezone.now()
        # If no end time, assume it ends when it starts for this check
        return self.start_time <= timezone.now()

    def is_ongoing(self):
        """Checks if the event is currently happening."""
        now = timezone.now()
        if self.end_time:
            return self.start_time <= now <= self.end_time
        return self.start_time <= now # If no end time, consider it ongoing once started

    def is_registration_open(self):
        """
        Checks if registration is currently open for the event.
        Considers if registration is required, if the event is upcoming,
        and if the deadline has passed.
        """
        if not self.registration_required or not self.is_published:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        return self.is_upcoming() # Registration is only active for upcoming events

    def get_remaining_capacity(self):
        """
        Calculates the remaining spots if registration is required and max_attendees is set.
        Requires a 'registrations' related name from a Registration model.
        """
        if not self.registration_required or self.max_attendees is None:
            return None # Capacity not relevant or not set

        # Assuming you have a related 'registrations' manager from a Registration model
        # For example, if you have a Registration model like:
        # class Registration(models.Model):
        #     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
        #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        current_registrations = self.registrations.count()
        return max(0, self.max_attendees - current_registrations)

    def is_full(self):
        """Checks if the event has reached its maximum attendance."""
        if self.max_attendees is None or not self.registration_required:
            return False
        remaining = self.get_remaining_capacity()
        return remaining is not None and remaining <= 0

    def formatted_start_datetime(self, format_str='%A, %B %d, %Y at %I:%M %p'):
        """Returns the start date and time formatted as a string."""
        return self.start_time.strftime(format_str)

    def formatted_end_datetime(self, format_str='%A, %B %d, %Y at %I:%M %p'):
        """Returns the end date and time formatted as a string."""
        if self.end_time:
            return self.end_time.strftime(format_str)
        return "N/A" # Or handle as desired if no end time

    def get_event_status(self):
        """Returns a string indicating the current status of the event."""
        if not self.is_published:
            return "Draft"
        if self.is_ongoing():
            return "Ongoing"
        if self.is_upcoming():
            return "Upcoming"
        if self.has_ended():
            return "Concluded"
        return "Scheduled"

    # --- Optional: Method to handle image cleanup ---
    # This method is often added to the model to delete the image file from storage
    # when the model instance is deleted or the image is changed.
    def clean_image_path(self):
        """Deletes the old image file when a new one is uploaded or the instance is deleted."""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)

    # Override the delete method to clean up the image file when the event is deleted
    def delete(self, *args, **kwargs):
        self.clean_image_path()
        super().delete(*args, **kwargs)

    # Override save method to clean up old image if a new one is uploaded
    def save(self, *args, **kwargs):
        if self.pk: # Only on existing instances
            old_event = Event.objects.get(pk=self.pk)
            if old_event.image and old_event.image != self.image:
                old_event.clean_image_path()
        super().save(*args, **kwargs)
        
        
        
        
class Beliefs(models.Model):
    icon  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    title  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    description  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    
    
        
class EventsHome(models.Model):
    title  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    image_text  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    date  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    description  = models.CharField(max_length=255, blank=True, null=True, help_text="")
    
    
    