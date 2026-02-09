"""
Management command to seed the database with sample data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from properties.models import Property
from reviews.models import Review
from team.models import TeamMember


class Command(BaseCommand):
    help = 'Seed the database with sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@nurastays.com',
                password='admin123',
                first_name='Nura',
                last_name='Admin',
            )
            self.stdout.write(self.style.SUCCESS('Created admin user (admin@nurastays.com / admin123)'))

        # Create properties
        properties_data = [
            {
                'name': 'Luxury Waterfront Apartment',
                'location': 'London, Canary Wharf',
                'description': 'Experience luxury living at its finest in this stunning waterfront apartment overlooking the Thames. This beautifully designed space features floor-to-ceiling windows, a fully equipped modern kitchen, and a spacious living area perfect for both business travelers and holidaymakers. The apartment is located in the heart of Canary Wharf, with easy access to restaurants, shops, and public transport. Wake up to breathtaking river views and enjoy the comfort of a hotel with the privacy of your own home.',
                'short_description': 'Stunning waterfront apartment with panoramic Thames views in the heart of Canary Wharf.',
                'price_per_night': 150.00,
                'bedrooms': 2,
                'bathrooms': 2,
                'max_guests': 4,
                'property_type': 'apartment',
                'amenities': ['WiFi', 'Smart TV', 'Kitchen', 'Washing Machine', 'Parking', 'Gym Access', 'Concierge', 'River View'],
                'house_rules': 'No smoking. No parties. Quiet hours 10pm-8am. Maximum 4 guests.',
                'cancellation_policy': 'Free cancellation up to 48 hours before check-in. After that, the first night is non-refundable.',
                'is_featured': True,
            },
            {
                'name': 'Cozy Studio in Shoreditch',
                'location': 'London, Shoreditch',
                'description': 'A charming and cozy studio apartment located in the vibrant heart of Shoreditch. Perfect for solo travelers or couples looking to explore East London\'s famous art scene, trendy cafes, and nightlife. The studio has been recently renovated with modern amenities while maintaining its characteristic charm. The space includes a comfortable double bed, a well-equipped kitchenette, and a stylish bathroom with a rain shower.',
                'short_description': 'Charming renovated studio in vibrant Shoreditch, perfect for exploring East London.',
                'price_per_night': 85.00,
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 2,
                'property_type': 'studio',
                'amenities': ['WiFi', 'Smart TV', 'Kitchenette', 'Washing Machine', 'Bike Storage', 'Coffee Machine'],
                'house_rules': 'No smoking. No pets. Quiet hours 11pm-7am.',
                'cancellation_policy': 'Free cancellation up to 24 hours before check-in.',
                'is_featured': True,
            },
            {
                'name': 'Elegant Victorian House',
                'location': 'Manchester, Didsbury',
                'description': 'Step into this beautifully restored Victorian house that perfectly blends period features with modern comfort. Spread across three floors, this spacious property offers plenty of room for families or groups of friends. The house features original fireplaces, high ceilings, and a lovely private garden. Located in the charming village of Didsbury, you\'ll find excellent restaurants, boutique shops, and beautiful parks on your doorstep.',
                'short_description': 'Beautifully restored Victorian house with private garden in charming Didsbury village.',
                'price_per_night': 200.00,
                'bedrooms': 4,
                'bathrooms': 3,
                'max_guests': 8,
                'property_type': 'house',
                'amenities': ['WiFi', 'Smart TV', 'Full Kitchen', 'Washing Machine', 'Dryer', 'Private Garden', 'Free Parking', 'BBQ', 'Pet Friendly'],
                'house_rules': 'Pets welcome (max 2). No smoking indoors. No parties or events.',
                'cancellation_policy': 'Free cancellation up to 7 days before check-in. 50% refund for cancellations up to 48 hours before.',
                'is_featured': True,
            },
            {
                'name': 'Modern City Centre Flat',
                'location': 'Birmingham, City Centre',
                'description': 'A sleek and modern apartment in the heart of Birmingham city centre. This newly built flat offers stunning city views, contemporary furnishings, and all the amenities you need for a comfortable stay. Located within walking distance of the Bullring, New Street Station, and the Jewellery Quarter. The building features a resident gym and secure underground parking.',
                'short_description': 'Sleek modern flat with city views, walking distance to all Birmingham attractions.',
                'price_per_night': 95.00,
                'bedrooms': 1,
                'bathrooms': 1,
                'max_guests': 3,
                'property_type': 'apartment',
                'amenities': ['WiFi', 'Smart TV', 'Kitchen', 'Gym Access', 'Secure Parking', 'Lift Access', 'Air Conditioning'],
                'house_rules': 'No smoking. No parties. Check-in after 3pm, check-out by 11am.',
                'cancellation_policy': 'Free cancellation up to 48 hours before check-in.',
                'is_featured': True,
            },
            {
                'name': 'Seaside Retreat Cottage',
                'location': 'Brighton, Kemptown',
                'description': 'Escape to this delightful seaside cottage just a stone\'s throw from Brighton beach. This charming two-bedroom cottage has been lovingly renovated to create a perfect coastal retreat. Enjoy morning coffee in the sunny courtyard garden, take a short walk to the famous Brighton Pier, or explore the eclectic shops and restaurants of Kemptown village.',
                'short_description': 'Delightful coastal cottage minutes from Brighton beach with sunny courtyard garden.',
                'price_per_night': 130.00,
                'bedrooms': 2,
                'bathrooms': 1,
                'max_guests': 4,
                'property_type': 'cottage',
                'amenities': ['WiFi', 'Smart TV', 'Full Kitchen', 'Courtyard Garden', 'BBQ', 'Beach Towels', 'Board Games'],
                'house_rules': 'No smoking. No pets. Respect the neighbours. Maximum 4 guests.',
                'cancellation_policy': 'Free cancellation up to 72 hours before check-in.',
                'is_featured': False,
            },
            {
                'name': 'Penthouse Suite with Skyline Views',
                'location': 'London, South Bank',
                'description': 'Indulge in this spectacular penthouse suite offering unrivalled panoramic views of the London skyline. This premium two-bedroom apartment features a wraparound terrace, designer interiors, and state-of-the-art amenities. Located on the South Bank, you\'re steps away from the Tate Modern, Shakespeare\'s Globe, and Borough Market. Perfect for special occasions or those seeking an extraordinary London experience.',
                'short_description': 'Spectacular penthouse with wraparound terrace and panoramic London skyline views.',
                'price_per_night': 350.00,
                'bedrooms': 2,
                'bathrooms': 2,
                'max_guests': 4,
                'property_type': 'penthouse',
                'amenities': ['WiFi', 'Smart TV', 'Full Kitchen', 'Terrace', 'Concierge', 'Gym', 'Spa Access', 'Parking', 'Air Conditioning', 'Nespresso Machine'],
                'house_rules': 'No smoking. No parties. No pets. Quiet hours 10pm-8am.',
                'cancellation_policy': 'Free cancellation up to 7 days before check-in. No refund within 7 days.',
                'is_featured': False,
            },
        ]

        for prop_data in properties_data:
            if not Property.objects.filter(name=prop_data['name']).exists():
                Property.objects.create(**prop_data)
                self.stdout.write(f"  Created property: {prop_data['name']}")

        # Create reviews
        properties = Property.objects.all()
        reviews_data = [
            {'guest_name': 'Sarah M.', 'rating': 5, 'review_text': 'Absolutely wonderful stay! The apartment was spotlessly clean, beautifully decorated, and had everything we needed. The location was perfect - walking distance to so many great restaurants and shops. Will definitely be booking again!'},
            {'guest_name': 'James T.', 'rating': 5, 'review_text': 'We had an amazing experience at this property. The host was incredibly responsive and helpful. The space was even better than the photos suggested. It truly felt like a home away from home.'},
            {'guest_name': 'Emily R.', 'rating': 4, 'review_text': 'Great property in a fantastic location. The apartment was well-equipped and very comfortable. Only minor issue was some noise from the street on Friday night, but overall an excellent stay.'},
            {'guest_name': 'David K.', 'rating': 5, 'review_text': 'Nura Stays really delivers on their promise. The property was immaculate, the check-in process was seamless, and the attention to detail was impressive. Luxury hotel quality with the comfort and privacy of your own space.'},
            {'guest_name': 'Priya S.', 'rating': 5, 'review_text': 'This was our second booking with Nura Stays and once again they exceeded our expectations. The property was gorgeous and the whole experience from booking to checkout was effortless. Highly recommend!'},
            {'guest_name': 'Michael B.', 'rating': 4, 'review_text': 'Very nice apartment with great amenities. The kitchen was fully stocked which was a nice touch. Location was convenient for our business meetings. Would happily stay here again.'},
            {'guest_name': 'Aisha N.', 'rating': 5, 'review_text': 'Perfect for our family holiday! The kids loved the space and we loved the comfort. Everything was thought of - from the welcome pack to the local recommendations guide. Thank you Nura Stays!'},
            {'guest_name': 'Tom W.', 'rating': 4, 'review_text': 'Clean, modern, and well-located property. Check-in was straightforward and the communication was excellent throughout. Good value for money compared to hotels in the area.'},
            {'guest_name': 'Rachel G.', 'rating': 5, 'review_text': 'Stunning property with incredible views! We booked this for our anniversary and it was absolutely perfect. The terrace was a real highlight. Already planning our next stay with Nura Stays.'},
            {'guest_name': 'Chris L.', 'rating': 5, 'review_text': 'I travel frequently for work and Nura Stays has become my go-to accommodation provider. Consistently high quality, great locations, and exceptional service. The gym access was a great bonus!'},
        ]

        if Review.objects.count() == 0:
            for i, review_data in enumerate(reviews_data):
                prop = properties[i % len(properties)] if properties.exists() else None
                Review.objects.create(property=prop, **review_data)
                self.stdout.write(f"  Created review by: {review_data['guest_name']}")

        # Create team members
        team_data = [
            {
                'name': 'Nura Ahmed',
                'role': 'Founder & CEO',
                'bio': 'Nura founded Nura Stays with a vision to provide exceptional short-term accommodation that combines hotel-level comfort with the warmth of a real home. With over 10 years of experience in property management and hospitality, she leads the company with passion and dedication.',
                'order_index': 1,
                'social_links': {'linkedin': '#', 'twitter': '#'},
            },
            {
                'name': 'Daniel Brooks',
                'role': 'Operations Manager',
                'bio': 'Daniel ensures every property meets our high standards and every guest has a seamless experience. His background in luxury hospitality brings a keen eye for detail and an unwavering commitment to guest satisfaction.',
                'order_index': 2,
                'social_links': {'linkedin': '#'},
            },
            {
                'name': 'Sophie Chen',
                'role': 'Property Acquisitions',
                'bio': 'Sophie scouts and secures the best properties for Nura Stays portfolio. With her expertise in real estate and an eye for potential, she ensures every new addition meets our quality standards and offers something special to our guests.',
                'order_index': 3,
                'social_links': {'linkedin': '#'},
            },
            {
                'name': 'Marcus Johnson',
                'role': 'Guest Experience Lead',
                'bio': 'Marcus is dedicated to ensuring every guest has an unforgettable experience. From the moment of booking to checkout, he oversees every touchpoint to deliver warmth, professionalism, and that personal touch that sets Nura Stays apart.',
                'order_index': 4,
                'social_links': {'linkedin': '#', 'instagram': '#'},
            },
        ]

        if TeamMember.objects.count() == 0:
            for member_data in team_data:
                TeamMember.objects.create(**member_data)
                self.stdout.write(f"  Created team member: {member_data['name']}")

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
