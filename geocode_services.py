#!/usr/bin/env python3
"""
Geocode Integrative Oncology Services
Adds latitude and longitude coordinates to all service addresses
"""

import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json

def geocode_address(geolocator, address, max_retries=3):
    """
    Geocode an address with retry logic
    """
    for attempt in range(max_retries):
        try:
            # Add delay to respect rate limits (1 request per second)
            time.sleep(1.1)

            location = geolocator.geocode(address, timeout=10)

            if location:
                return {
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'geocode_accuracy': 'high',
                    'geocode_source': 'Nominatim',
                    'display_name': location.address
                }
            else:
                return {
                    'latitude': None,
                    'longitude': None,
                    'geocode_accuracy': 'failed',
                    'geocode_source': 'Nominatim',
                    'display_name': None
                }

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"  ⚠️  Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
                continue
            else:
                return {
                    'latitude': None,
                    'longitude': None,
                    'geocode_accuracy': 'error',
                    'geocode_source': 'Nominatim',
                    'display_name': None
                }

def main():
    print("🗺️  Integrative Oncology Services Geocoding")
    print("=" * 60)

    # Initialize geocoder
    print("\n1. Initializing geocoder...")
    geolocator = Nominatim(
        user_agent="integrative-oncology-services-research-v1.0",
        timeout=10
    )
    print("   ✓ Nominatim geocoder initialized")

    # Load data
    print("\n2. Loading service data...")
    df = pd.read_csv('data/integrative_oncology_services.csv')
    print(f"   ✓ Loaded {len(df)} services")

    # Prepare geocoding
    print("\n3. Starting geocoding process...")
    print("   Note: This will take ~25 seconds (respecting 1 req/sec rate limit)")
    print()

    geocoded_results = []
    failed_count = 0

    for idx, row in df.iterrows():
        # Construct full address
        address_parts = [
            str(row['Address']) if pd.notna(row['Address']) else '',
            str(row['Suburb']) if pd.notna(row['Suburb']) else '',
            'SA' if pd.notna(row['Suburb']) else '',  # Assuming South Australia for now
            str(int(row['Postcode'])) if pd.notna(row['Postcode']) else '',
            'Australia'
        ]
        full_address = ', '.join([p for p in address_parts if p])

        print(f"   [{idx + 1}/{len(df)}] Geocoding: {row['Name'][:40]}...")
        print(f"       Address: {full_address[:70]}")

        # Geocode
        geocode_result = geocode_address(geolocator, full_address)

        if geocode_result['latitude']:
            print(f"       ✓ Success: ({geocode_result['latitude']:.6f}, {geocode_result['longitude']:.6f})")
        else:
            print(f"       ✗ Failed to geocode")
            failed_count += 1

        geocoded_results.append(geocode_result)
        print()

    # Add geocoding results to dataframe
    print("\n4. Adding coordinates to dataset...")
    df['latitude'] = [r['latitude'] for r in geocoded_results]
    df['longitude'] = [r['longitude'] for r in geocoded_results]
    df['geocode_accuracy'] = [r['geocode_accuracy'] for r in geocoded_results]
    df['geocode_source'] = [r['geocode_source'] for r in geocoded_results]
    df['geocode_display_name'] = [r['display_name'] for r in geocoded_results]

    # Save geocoded data
    print("\n5. Saving geocoded data...")

    # Save as CSV
    output_csv = 'data/services_geocoded.csv'
    df.to_csv(output_csv, index=False)
    print(f"   ✓ Saved CSV: {output_csv}")

    # Save as JSON for web application
    output_json = 'data/services_geocoded.json'
    df_json = df.to_dict('records')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(df_json, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved JSON: {output_json}")

    # Save Excel with geocoded data
    output_excel = 'Data_geocoded.xlsx'
    df.to_excel(output_excel, index=False, engine='openpyxl')
    print(f"   ✓ Saved Excel: {output_excel}")

    # Print summary
    print("\n" + "=" * 60)
    print("📊 GEOCODING SUMMARY")
    print("=" * 60)
    print(f"Total services:        {len(df)}")
    print(f"Successfully geocoded: {len(df) - failed_count}")
    print(f"Failed to geocode:     {failed_count}")
    print(f"Success rate:          {((len(df) - failed_count) / len(df) * 100):.1f}%")

    if failed_count > 0:
        print("\n⚠️  Failed addresses:")
        failed_df = df[df['latitude'].isna()]
        for idx, row in failed_df.iterrows():
            print(f"   - {row['Name']}")
            print(f"     Address: {row['Address']}, {row['Suburb']} {row['Postcode']}")

    print("\n✅ Geocoding complete!")
    print(f"\n📁 Output files:")
    print(f"   - {output_csv}")
    print(f"   - {output_json}")
    print(f"   - {output_excel}")
    print("\n🚀 Ready to build the application!")

if __name__ == '__main__':
    main()
