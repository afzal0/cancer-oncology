#!/usr/bin/env python3
"""
Manually fix failed geocoding attempts with more specific addresses
"""

import pandas as pd
import time
from geopy.geocoders import Nominatim
import json

def geocode_address(geolocator, address):
    """Geocode an address"""
    time.sleep(1.1)
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude, location.address
    except:
        pass
    return None, None, None

# Manual address corrections for failed geocoding
MANUAL_FIXES = {
    'Youth Cancer Service SA/NT': '72 King William Road, North Adelaide SA 5006, Australia',  # Same as WCH
    'Flinders Cancer Wellness Centre': 'Flinders Drive, Bedford Park SA 5042, Australia',  # Flinders Medical Centre
    'Redkite SA': '202 Greenhill Road, Eastwood SA 5063, Australia',  # Cancer Council SA location
    'Under Our Roof Accommodation': 'Woodville Road, Woodville West SA 5011, Australia',
    'UniSA Psychology Clinic': 'St Bernards Road, Magill SA 5072, Australia',
    'Flinders University Psychology Clinic': 'Sturt Road, Bedford Park SA 5042, Australia',
    'Look Good Feel Better SA': '202 Greenhill Road, Eastwood SA 5063, Australia',  # Cancer Council SA
    'Starlight Children\'s Foundation SA': '72 King William Road, North Adelaide SA 5006, Australia'  # WCH
}

def main():
    print("🔧 Fixing Failed Geocoding Attempts")
    print("=" * 60)

    # Initialize geocoder
    geolocator = Nominatim(
        user_agent="integrative-oncology-services-research-v1.0",
        timeout=10
    )

    # Load geocoded data
    df = pd.read_csv('data/services_geocoded.csv')

    # Find failed geocodes
    failed = df[df['latitude'].isna()]
    print(f"\nFound {len(failed)} services to fix\n")

    # Fix each one
    for idx, row in failed.iterrows():
        service_name = row['Name']

        if service_name in MANUAL_FIXES:
            corrected_address = MANUAL_FIXES[service_name]
            print(f"Fixing: {service_name}")
            print(f"   New address: {corrected_address}")

            lat, lon, display_name = geocode_address(geolocator, corrected_address)

            if lat:
                df.at[idx, 'latitude'] = lat
                df.at[idx, 'longitude'] = lon
                df.at[idx, 'geocode_accuracy'] = 'manual_fix'
                df.at[idx, 'geocode_source'] = 'Nominatim'
                df.at[idx, 'geocode_display_name'] = display_name
                print(f"   ✓ Success: ({lat:.6f}, {lon:.6f})\n")
            else:
                print(f"   ✗ Still failed\n")

    # Save updated data
    df.to_csv('data/services_geocoded.csv', index=False)

    df_json = df.to_dict('records')
    with open('data/services_geocoded.json', 'w', encoding='utf-8') as f:
        json.dump(df_json, f, indent=2, ensure_ascii=False)

    df.to_excel('Data_geocoded.xlsx', index=False, engine='openpyxl')

    # Print final summary
    total = len(df)
    successful = len(df[df['latitude'].notna()])
    failed = len(df[df['latitude'].isna()])

    print("=" * 60)
    print("📊 FINAL GEOCODING SUMMARY")
    print("=" * 60)
    print(f"Total services:        {total}")
    print(f"Successfully geocoded: {successful}")
    print(f"Failed to geocode:     {failed}")
    print(f"Success rate:          {(successful / total * 100):.1f}%")

    if failed > 0:
        print("\n⚠️  Still failed:")
        failed_df = df[df['latitude'].isna()]
        for idx, row in failed_df.iterrows():
            print(f"   - {row['Name']}")

    print("\n✅ Update complete!")

if __name__ == '__main__':
    main()
