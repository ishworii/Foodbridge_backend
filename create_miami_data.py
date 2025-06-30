#!/usr/bin/env python
import os
import random
import sys
from datetime import datetime, timedelta
from decimal import Decimal

import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "foodbridge.settings")
django.setup()

from core.models import Donation, Profile
from django.contrib.auth.models import User


def create_users():
    """Create 10 donors and 7 receivers"""
    users_data = [
        # Donors
        {
            "username": "miami_restaurant",
            "email": "miami_restaurant@example.com",
            "role": "donor",
        },
        {
            "username": "fresh_market",
            "email": "fresh_market@example.com",
            "role": "donor",
        },
        {
            "username": "organic_farm",
            "email": "organic_farm@example.com",
            "role": "donor",
        },
        {
            "username": "bakery_downtown",
            "email": "bakery_downtown@example.com",
            "role": "donor",
        },
        {
            "username": "cafe_south_beach",
            "email": "cafe_south_beach@example.com",
            "role": "donor",
        },
        {
            "username": "grocery_store",
            "email": "grocery_store@example.com",
            "role": "donor",
        },
        {
            "username": "food_truck",
            "email": "food_truck@example.com",
            "role": "donor",
        },
        {
            "username": "catering_service",
            "email": "catering_service@example.com",
            "role": "donor",
        },
        {
            "username": "farmers_market",
            "email": "farmers_market@example.com",
            "role": "donor",
        },
        {
            "username": "community_garden",
            "email": "community_garden@example.com",
            "role": "donor",
        },
        # Receivers
        {
            "username": "soup_kitchen",
            "email": "soup_kitchen@example.com",
            "role": "receiver",
        },
        {
            "username": "food_bank",
            "email": "food_bank@example.com",
            "role": "receiver",
        },
        {
            "username": "homeless_shelter",
            "email": "homeless_shelter@example.com",
            "role": "receiver",
        },
        {
            "username": "community_center",
            "email": "community_center@example.com",
            "role": "receiver",
        },
        {
            "username": "church_outreach",
            "email": "church_outreach@example.com",
            "role": "receiver",
        },
        {
            "username": "senior_center",
            "email": "senior_center@example.com",
            "role": "receiver",
        },
        {
            "username": "youth_program",
            "email": "youth_program@example.com",
            "role": "receiver",
        },
    ]

    users = []
    for user_data in users_data:
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password="password123",
        )
        # Set the role on the auto-created profile
        user.profile.role = user_data["role"]
        user.profile.save()
        users.append(user)
        print(f"Created user: {user.username} ({user_data['role']})")

    return users


def get_miami_locations():
    """Get realistic locations within 100 miles of Miami"""
    # Miami coordinates: 25.7617° N, 80.1918° W
    miami_lat, miami_lng = 25.7617, -80.1918

    locations = [
        # Miami area
        {"name": "Downtown Miami", "lat": 25.7617, "lng": -80.1918},
        {"name": "South Beach", "lat": 25.7907, "lng": -80.1300},
        {"name": "Coral Gables", "lat": 25.7215, "lng": -80.2684},
        {"name": "Miami Beach", "lat": 25.7907, "lng": -80.1300},
        {"name": "Brickell", "lat": 25.7617, "lng": -80.1918},
        {"name": "Wynwood", "lat": 25.8015, "lng": -80.1992},
        {"name": "Little Havana", "lat": 25.7617, "lng": -80.1918},
        {"name": "Coconut Grove", "lat": 25.7289, "lng": -80.2378},
        {"name": "Key Biscayne", "lat": 25.6907, "lng": -80.1628},
        {"name": "North Miami", "lat": 25.8901, "lng": -80.1865},
        # Fort Lauderdale area
        {"name": "Fort Lauderdale", "lat": 26.1224, "lng": -80.1373},
        {"name": "Hollywood, FL", "lat": 26.0112, "lng": -80.1495},
        {"name": "Pompano Beach", "lat": 26.2379, "lng": -80.1248},
        {"name": "Deerfield Beach", "lat": 26.3184, "lng": -80.0992},
        # West Palm Beach area
        {"name": "West Palm Beach", "lat": 26.7153, "lng": -80.0534},
        {"name": "Boca Raton", "lat": 26.3683, "lng": -80.1289},
        {"name": "Delray Beach", "lat": 26.4615, "lng": -80.0728},
        {"name": "Boynton Beach", "lat": 26.5317, "lng": -80.0905},
        # Homestead area
        {"name": "Homestead", "lat": 25.4687, "lng": -80.4776},
        {"name": "Florida City", "lat": 25.4479, "lng": -80.4792},
        {"name": "Key Largo", "lat": 25.0865, "lng": -80.4473},
        # Hialeah area
        {"name": "Hialeah", "lat": 25.8576, "lng": -80.2781},
        {"name": "Miami Gardens", "lat": 25.9420, "lng": -80.2456},
        {"name": "Opa-locka", "lat": 25.9023, "lng": -80.2503},
    ]

    return locations


def get_food_types():
    """Get food type categories"""
    return [
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
        "other",
    ]


def get_rich_descriptions():
    """Get rich text descriptions for donations"""
    descriptions = [
        "<p><strong>Fresh Organic Produce</strong></p><p>Locally grown organic vegetables and fruits. Perfect for healthy meals and smoothies. All items are pesticide-free and harvested within the last 24 hours.</p><ul><li>Fresh from our garden</li><li>No pesticides used</li><li>Great for families</li></ul>",
        "<p><strong>Artisan Bread Selection</strong></p><p>Freshly baked artisan breads made with premium ingredients. Includes sourdough, whole wheat, and specialty loaves. Perfect for sandwiches or as a side dish.</p><ul><li>Made fresh daily</li><li>No preservatives</li><li>Multiple varieties available</li></ul>",
        "<p><strong>Dairy Products</strong></p><p>Fresh dairy products including milk, cheese, and yogurt. All products are from local farms and within their best-by dates.</p><ul><li>Local farm fresh</li><li>Properly refrigerated</li><li>Great nutritional value</li></ul>",
        "<p><strong>Canned Goods Collection</strong></p><p>Assorted canned goods including vegetables, fruits, and proteins. Perfect for emergency food supplies or regular meals.</p><ul><li>Long shelf life</li><li>Nutritious options</li><li>Easy to store</li></ul>",
        "<p><strong>Frozen Foods</strong></p><p>Frozen vegetables, fruits, and prepared meals. All items are properly frozen and maintained at optimal temperatures.</p><ul><li>Flash frozen for freshness</li><li>Convenient meal options</li><li>Preserves nutrients</li></ul>",
        "<p><strong>Fresh Meat & Protein</strong></p><p>Fresh meat and protein sources including chicken, beef, and fish. All items are properly handled and within safe consumption dates.</p><ul><li>Properly stored</li><li>High quality protein</li><li>Safe handling practices</li></ul>",
        "<p><strong>Beverages & Drinks</strong></p><p>Assorted beverages including juices, water, and healthy drinks. Perfect for hydration and nutrition.</p><ul><li>Various options available</li><li>Good for all ages</li><li>Refreshing choices</li></ul>",
        "<p><strong>Snacks & Treats</strong></p><p>Healthy snacks and treats including nuts, dried fruits, and granola bars. Great for on-the-go nutrition.</p><ul><li>Portable options</li><li>Healthy ingredients</li><li>Kid-friendly choices</li></ul>",
        "<p><strong>Grain Products</strong></p><p>Various grain products including rice, pasta, and cereals. Essential staples for any kitchen.</p><ul><li>Long shelf life</li><li>Versatile ingredients</li><li>Good for bulk cooking</li></ul>",
        "<p><strong>Mixed Food Basket</strong></p><p>Assorted food items including a variety of fresh, canned, and packaged goods. Perfect for families or individuals in need.</p><ul><li>Diverse selection</li><li>Balanced nutrition</li><li>Something for everyone</li></ul>",
    ]
    return descriptions


def create_donations(users, locations):
    """Create 100 donations around Miami"""
    donors = [user for user in users if user.profile.role == "donor"]
    receivers = [
        user for user in users if user.profile.role == "receiver"
    ]
    food_types = get_food_types()
    descriptions = get_rich_descriptions()

    # Miami coordinates for distance calculation
    miami_lat, miami_lng = 25.7617, -80.1918

    donations = []
    for i in range(100):
        # Random donor
        donor = random.choice(donors)

        # Random location
        location_data = random.choice(locations)

        # Add some random variation to coordinates (±0.1 degrees ≈ 6-7 miles)
        lat_variation = random.uniform(-0.1, 0.1)
        lng_variation = random.uniform(-0.1, 0.1)

        latitude = location_data["lat"] + lat_variation
        longitude = location_data["lng"] + lng_variation

        # Random food type
        food_type = random.choice(food_types)

        # Random quantity (1-20)
        quantity = random.randint(1, 20)

        # Random expiry date (within next 30 days)
        days_to_expiry = random.randint(1, 30)
        expiry_date = datetime.now().date() + timedelta(
            days=days_to_expiry
        )

        # Random description
        description = random.choice(descriptions)

        # Create donation
        donation = Donation.objects.create(
            donor=donor,
            title=f"Food Donation #{i+1} - {food_type.title()}",
            description=description,
            quantity=quantity,
            location=f"{location_data['name']}, FL",
            latitude=latitude,
            longitude=longitude,
            food_type=food_type,
            expiry_date=expiry_date,
            is_claimed=False,
            created_at=datetime.now()
            - timedelta(days=random.randint(0, 7)),
        )

        donations.append(donation)
        print(
            f"Created donation: {donation.title} by {donor.username}"
        )

    return donations


def claim_donations(donations, receivers):
    """Claim 70 random donations"""
    # Randomly select 70 donations to claim
    donations_to_claim = random.sample(donations, 70)

    for donation in donations_to_claim:
        receiver = random.choice(receivers)
        donation.is_claimed = True
        donation.claimed_by = receiver
        donation.save()
        print(
            f"Claimed donation: {donation.title} by {receiver.username}"
        )


def main():
    print("Creating Miami FoodBridge data...")

    # Clear existing data
    print("Clearing existing data...")
    Donation.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.all().delete()

    # Create users
    print("\nCreating users...")
    users = create_users()

    # Get locations
    locations = get_miami_locations()

    # Create donations
    print("\nCreating donations...")
    donations = create_donations(users, locations)

    # Claim donations
    print("\nClaiming donations...")
    receivers = [
        user for user in users if user.profile.role == "receiver"
    ]
    claim_donations(donations, receivers)

    # Print summary
    print("\n" + "=" * 50)
    print("DATA CREATION COMPLETE!")
    print("=" * 50)
    print(f"Total Users: {User.objects.count()}")
    print(
        f"  - Donors: {User.objects.filter(profile__role='donor').count()}"
    )
    print(
        f"  - Receivers: {User.objects.filter(profile__role='receiver').count()}"
    )
    print(f"Total Donations: {Donation.objects.count()}")
    print(
        f"  - Available: {Donation.objects.filter(is_claimed=False).count()}"
    )
    print(
        f"  - Claimed: {Donation.objects.filter(is_claimed=True).count()}"
    )
    print(
        f"Claim Rate: {(Donation.objects.filter(is_claimed=True).count() / Donation.objects.count()) * 100:.1f}%"
    )
    print("=" * 50)


if __name__ == "__main__":
    main()
