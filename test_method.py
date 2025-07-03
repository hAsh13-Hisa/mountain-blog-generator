#!/usr/bin/env python3
"""
Test script to check if generate_basic_site_from_database method exists
"""
from affiliate_static_generator import AffiliateStaticGenerator

# Create generator instance
generator = AffiliateStaticGenerator()

# Check if method exists
if hasattr(generator, 'generate_basic_site_from_database'):
    print("✅ Method exists")
    print(f"🗂️ Database has {generator.mountains_data['metadata']['total_mountains']} mountains")
    
    # Try to call the method
    try:
        generator.generate_basic_site_from_database()
        print("✅ Method executed successfully")
    except Exception as e:
        print(f"❌ Error executing method: {e}")
else:
    print("❌ Method does not exist")
    print("Available methods:", [method for method in dir(generator) if not method.startswith('_')])