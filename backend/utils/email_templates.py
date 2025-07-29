from flask import render_template_string
from datetime import datetime

def render_daily_reminder_html(user, bookings_today=None):
    template = """
    <h2>Good morning, {{ user.name }} 👋</h2>

    {% if bookings_today %}
        <p>Here is your parking schedule for <strong>{{ today }}</strong>:</p>
        <ul>
            {% for booking in bookings_today %}
                <li>
                    <strong>{{ booking.location_name }}</strong> at {{ booking.time.strftime('%I:%M %p') }} 
                    (Vehicle: {{ booking.vehicle_number }})
                </li>
            {% endfor %}
        </ul>
        <p>Make sure to arrive 5 minutes early. Have a great day! 🚗</p>
    {% else %}
        <p>You don’t have any bookings today. Need a spot? <a href="https://parkeasy.in/book">Book Now</a>!</p>
    {% endif %}

    <hr>
    <p style="font-size: 0.9em; color: gray;">
        This is an automated message from ParkEasy. Manage your notifications <a href="https://parkeasy.in/settings">here</a>.
    </p>
    """
    
    return render_template_string(
        template,
        user=user,
        bookings_today=bookings_today or [],
        today=datetime.now().strftime('%A, %B %d, %Y')
    )
