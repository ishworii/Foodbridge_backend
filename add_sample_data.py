#!/usr/bin/env python
"""
Script to add sample donation data with coordinates for testing map functionality.
Run this script after setting up the database and creating a superuser.
"""

import os
import random
import sys
from datetime import datetime, timedelta

import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodbridge.settings")
django.setup()

from core.models import Donation, Profile
from django.contrib.auth.models import User


def create_sample_data():
    """Create sample donation data with coordinates around Boston area"""

    # Get or create a test user
    user, created = User.objects.get_or_create(
        username="test_donor",
        defaults={
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "Donor",
        },
    )

    if created:
        user.set_password("testpass123")
        user.save()

        # Create profile
        Profile.objects.create(user=user, role="donor")
        print(f"Created test user: {user.username}")
    else:
        # Ensure profile exists
        profile, profile_created = Profile.objects.get_or_create(
            user=user, defaults={"role": "donor"}
        )
        if profile_created:
            print(
                f"Created profile for existing user: {user.username}"
            )
        else:
            print(f"Using existing user: {user.username}")

    # Sample locations around Boston (latitude, longitude)
    boston_locations = [
        (42.3601, -71.0589),  # Downtown Boston
        (42.3651, -71.0639),  # North End
        (42.3551, -71.0539),  # South End
        (42.3701, -71.0689),  # Charlestown
        (42.3501, -71.0489),  # Back Bay
        (42.3751, -71.0739),  # East Boston
        (42.3451, -71.0439),  # Fenway
        (42.3801, -71.0789),  # Cambridge
        (42.3401, -71.0389),  # Brookline
        (42.3851, -71.0839),  # Somerville
        (42.3351, -71.0339),  # Newton
        (42.3901, -71.0889),  # Medford
        (42.3301, -71.0289),  # Watertown
        (42.3951, -71.0939),  # Arlington
        (42.3251, -71.0239),  # Waltham
    ]

    # Food types
    food_types = [
        "fruits",
        "vegetables",
        "grains",
        "dairy",
        "meat",
        "baked goods",
        "canned goods",
        "frozen foods",
        "beverages",
        "snacks",
    ]

    # Sample donation titles
    donation_titles = [
        "Fresh Apples and Oranges",
        "Organic Vegetables Bundle",
        "Whole Grain Bread",
        "Milk and Cheese",
        "Chicken and Beef",
        "Homemade Cookies",
        "Canned Soup and Beans",
        "Frozen Vegetables",
        "Juice and Soda",
        "Crackers and Chips",
        "Bananas and Berries",
        "Fresh Tomatoes",
        "Rice and Pasta",
        "Yogurt and Butter",
        "Pork and Turkey",
        "Fresh Baked Muffins",
        "Canned Tuna and Salmon",
        "Frozen Pizza",
        "Water and Tea",
        "Nuts and Dried Fruits",
    ]

    # Create sample donations
    donations_created = 0

    for i, (lat, lng) in enumerate(boston_locations):
        # Create multiple donations per location
        for j in range(random.randint(1, 3)):
            title = random.choice(donation_titles)
            food_type = random.choice(food_types)

            # Random expiry date (within next 30 days)
            expiry_date = datetime.now().date() + timedelta(
                days=random.randint(1, 30)
            )

            # Random quantity
            quantity = random.randint(1, 10)

            # Random location name
            location_names = [
                "Downtown Boston",
                "North End",
                "South End",
                "Charlestown",
                "Back Bay",
                "East Boston",
                "Fenway",
                "Cambridge",
                "Brookline",
                "Somerville",
                "Newton",
                "Medford",
                "Watertown",
                "Arlington",
                "Waltham",
            ]
            location = random.choice(location_names)

            # Random claim status (20% chance of being claimed)
            is_claimed = random.random() < 0.2

            donation = Donation.objects.create(
                donor=user,
                title=f"{title} #{i+1}-{j+1}",
                description=f"Fresh {food_type} available for pickup. Expires on {expiry_date.strftime('%Y-%m-%d')}.",
                quantity=quantity,
                location=location,
                latitude=lat
                + random.uniform(-0.005, 0.005),  # Add some variation
                longitude=lng
                + random.uniform(-0.005, 0.005),  # Add some variation
                food_type=food_type,
                expiry_date=expiry_date,
                is_claimed=is_claimed,
                created_at=datetime.now()
                - timedelta(days=random.randint(0, 7)),
            )

            donations_created += 1
            print(
                f"Created donation: {donation.title} at ({donation.latitude:.4f}, {donation.longitude:.4f})"
            )

    print(f"\nCreated {donations_created} sample donations!")
    print(
        f"Test user credentials: username='test_donor', password='testpass123'"
    )


if __name__ == "__main__":
    create_sample_data()
