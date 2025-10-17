#!/usr/bin/env python3
"""
Geocode ALL Integrative Oncology Services across ALL Australian cities
Processes the complete dataset of 185 services
"""

import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json
import os

def geocode_address(geolocator, address, max_retries=3):
    """Geocode an address with retry logic"""
    for attempt in range(max_retries):
        try:
            time.sleep(1.1)  # Respect rate limits
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
                time.sleep(2)
                continue
            else:
                return {
                    'latitude': None,
                    'longitude': None,
                    'geocode_accuracy': 'error',
                    'geocode_source': 'Nominatim',
                    'display_name': None
                }

def detect_state(suburb, postcode):
    """Detect Australian state from postcode"""
    postcode = int(postcode) if pd.notna(postcode) else 0

    if 2000 <= postcode < 3000:
        return 'NSW'
    elif 3000 <= postcode < 4000:
        return 'VIC'
    elif 4000 <= postcode < 5000:
        return 'QLD'
    elif 5000 <= postcode < 6000:
        return 'SA'
    elif 6000 <= postcode < 7000:
        return 'WA'
    elif 7000 <= postcode < 8000:
        return 'TAS'
    elif 800 <= postcode < 900:
        return 'NT'
    else:
        return 'Australia'

def main():
    print("🗺️  Geocoding ALL Australian Integrative Oncology Services")
    print("=" * 70)

    # Check which file to use
    print("\n📁 Available data files:")
    files_to_check = [
        'Data_final_cleaned.xlsx',
        'Data_final.xlsx',
        'Data-sample.xlsx',
        'sydney_data.csv',
        'data/integrative_oncology_services.csv'
    ]

    available_files = []
    for f in files_to_check:
        if os.path.exists(f):
            try:
                if f.endswith('.csv'):
                    df_temp = pd.read_csv(f)
                else:
                    df_temp = pd.read_excel(f)
                print(f"   ✓ {f} ({len(df_temp)} records)")
                available_files.append((f, len(df_temp)))
            except:
                pass

    if not available_files:
        print("\n❌ No data files found!")
        print("\nPlease specify the file with ALL 185 services:")
        print("   - Place the complete dataset in the project root")
        print("   - Name it 'all_services_complete.xlsx' or similar")
        return

    # Ask user which file to geocode
    print("\n" + "=" * 70)
    print("IMPORTANT: Which file contains the COMPLETE dataset (185 services)?")
    print("=" * 70)
    for idx, (filename, count) in enumerate(available_files):
        print(f"{idx + 1}. {filename} ({count} records)")

    print("\nEdit this script and set the filename below, then run again:")
    print("   INPUT_FILE = 'your_complete_dataset.xlsx'")
    return

    # Initialize geocoder
    print("\n1. Initializing geocoder...")
    geolocator = Nominatim(
        user_agent="integrative-oncology-services-australia-v1.0",
        timeout=10
    )
    print("   ✓ Nominatim geocoder initialized")

    # Load data
    # CHANGE THIS LINE TO YOUR COMPLETE DATASET FILE:
    INPUT_FILE = 'Data_final_cleaned.xlsx'  # ← CHANGE THIS

    print(f"\n2. Loading service data from: {INPUT_FILE}")

    if INPUT_FILE.endswith('.csv'):
        df = pd.read_csv(INPUT_FILE)
    else:
        df = pd.read_excel(INPUT_FILE)

    print(f"   ✓ Loaded {len(df)} services")

    # Add State column if not present
    if 'State' not in df.columns:
        print("\n3. Adding State information based on postcodes...")
        df['State'] = df.apply(lambda row: detect_state(row['Suburb'], row['Postcode']), axis=1)
        print("   ✓ State column added")

    # Check for existing geocoded data
    if 'latitude' in df.columns and df['latitude'].notna().sum() > 0:
        already_geocoded = df['latitude'].notna().sum()
        print(f"\n⚠️  Found {already_geocoded} already geocoded services")
        print("   Will skip these and only geocode new services")
        to_geocode = df[df['latitude'].isna()]
    else:
        to_geocode = df.copy()
        df['latitude'] = None
        df['longitude'] = None
        df['geocode_accuracy'] = None
        df['geocode_source'] = None
        df['geocode_display_name'] = None

    total_to_geocode = len(to_geocode)
    print(f"\n4. Starting geocoding for {total_to_geocode} services...")
    print(f"   Estimated time: ~{total_to_geocode * 1.2 / 60:.1f} minutes")
    print("   (Respecting 1 request/second rate limit)\n")

    failed_count = 0

    for idx, row in to_geocode.iterrows():
        # Construct full address
        state = row.get('State', 'Australia')
        address_parts = [
            str(row['Address']) if pd.notna(row['Address']) else '',
            str(row['Suburb']) if pd.notna(row['Suburb']) else '',
            state,
            str(int(row['Postcode'])) if pd.notna(row['Postcode']) else '',
            'Australia'
        ]
        full_address = ', '.join([p for p in address_parts if p])

        print(f"   [{idx + 1}/{len(df)}] {row['Name'][:50]}")
        print(f"       📍 {full_address[:80]}")

        # Geocode
        result = geocode_address(geolocator, full_address)

        if result['latitude']:
            print(f"       ✓ ({result['latitude']:.6f}, {result['longitude']:.6f})")
            df.at[idx, 'latitude'] = result['latitude']
            df.at[idx, 'longitude'] = result['longitude']
            df.at[idx, 'geocode_accuracy'] = result['geocode_accuracy']
            df.at[idx, 'geocode_source'] = result['geocode_source']
            df.at[idx, 'geocode_display_name'] = result['display_name']
        else:
            print(f"       ✗ Failed")
            failed_count += 1
            df.at[idx, 'geocode_accuracy'] = result['geocode_accuracy']

        print()

    # Save results
    print("\n5. Saving geocoded data...")

    # CSV
    output_csv = 'data/all_services_geocoded.csv'
    os.makedirs('data', exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"   ✓ Saved CSV: {output_csv}")

    # JSON
    output_json = 'data/all_services_geocoded.json'
    df_json = df.to_dict('records')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(df_json, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Saved JSON: {output_json}")

    # Excel
    output_excel = 'All_Services_Geocoded.xlsx'
    df.to_excel(output_excel, index=False, engine='openpyxl')
    print(f"   ✓ Saved Excel: {output_excel}")

    # Summary
    total = len(df)
    successful = len(df[df['latitude'].notna()])
    failed = len(df[df['latitude'].isna()])

    print("\n" + "=" * 70)
    print("📊 GEOCODING SUMMARY")
    print("=" * 70)
    print(f"Total services:        {total}")
    print(f"Successfully geocoded: {successful}")
    print(f"Failed to geocode:     {failed}")
    print(f"Success rate:          {(successful / total * 100):.1f}%")

    # Breakdown by city
    if 'Suburb' in df.columns:
        print("\n📍 Services by location:")
        city_counts = df.groupby('Suburb').size().sort_values(ascending=False)
        for city, count in city_counts.head(10).items():
            geocoded_count = len(df[(df['Suburb'] == city) & (df['latitude'].notna())])
            print(f"   {city:20s} {geocoded_count}/{count} geocoded")

    if failed > 0:
        print(f"\n⚠️  {failed} addresses need manual review")
        print("   Run fix_failed_geocoding.py to manually correct them")

    print("\n✅ Geocoding complete!")
    print(f"\n📁 Output files:")
    print(f"   - {output_csv}")
    print(f"   - {output_json}")
    print(f"   - {output_excel}")

if __name__ == '__main__':
    main()
