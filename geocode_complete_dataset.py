#!/usr/bin/env python3
"""
Geocode ALL 185 Integrative Oncology Services from all 7 Australian cities
Reads from Data_final_cleaned.xlsx (7 sheets) and geocodes everything
"""

import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json

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

def detect_state(sheet_name):
    """Detect state from sheet name"""
    sheet_lower = sheet_name.lower()
    if 'sydney' in sheet_lower:
        return 'NSW'
    elif 'melbourne' in sheet_lower:
        return 'VIC'
    elif 'brisbane' in sheet_lower:
        return 'QLD'
    elif 'adelaide' in sheet_lower or 'adelaid' in sheet_lower:
        return 'SA'
    elif 'perth' in sheet_lower:
        return 'WA'
    elif 'hobart' in sheet_lower:
        return 'TAS'
    elif 'darwin' in sheet_lower:
        return 'NT'
    else:
        return 'Australia'

def main():
    print("🗺️  Geocoding ALL Australian Integrative Oncology Services")
    print("=" * 70)
    print("Source: Data_final_cleaned.xlsx (7 cities, 185 services)")
    print("=" * 70)

    # Load all sheets
    print("\n1. Loading data from all city sheets...")
    xl = pd.ExcelFile('Data_final_cleaned.xlsx')

    all_dfs = []
    for sheet_name in xl.sheet_names:
        df = pd.read_excel('Data_final_cleaned.xlsx', sheet_name=sheet_name)
        df['City_Sheet'] = sheet_name
        df['State'] = detect_state(sheet_name)
        all_dfs.append(df)
        print(f"   ✓ {sheet_name}: {len(df)} records")

    # Combine all sheets
    df_all = pd.concat(all_dfs, ignore_index=True)
    print(f"\n   📊 Total services loaded: {len(df_all)}")

    # Initialize geocoder
    print("\n2. Initializing geocoder...")
    geolocator = Nominatim(
        user_agent="integrative-oncology-australia-research-v1.0",
        timeout=10
    )
    print("   ✓ Nominatim geocoder ready")

    # Add geocoding columns
    df_all['latitude'] = None
    df_all['longitude'] = None
    df_all['geocode_accuracy'] = None
    df_all['geocode_source'] = None
    df_all['geocode_display_name'] = None

    # Geocode all services
    print(f"\n3. Geocoding {len(df_all)} services...")
    print(f"   ⏱️  Estimated time: ~{len(df_all) * 1.2 / 60:.1f} minutes")
    print("   (Respecting 1 request/second rate limit)\n")

    failed_count = 0
    city_stats = {}

    for idx, row in df_all.iterrows():
        # Track by city
        city_sheet = row['City_Sheet']
        if city_sheet not in city_stats:
            city_stats[city_sheet] = {'total': 0, 'success': 0, 'failed': 0}
        city_stats[city_sheet]['total'] += 1

        # Construct full address
        state = row['State']

        # Handle postcode - convert to string, handle non-numeric values
        postcode_val = ''
        if pd.notna(row['Postcode']):
            try:
                postcode_val = str(int(row['Postcode']))
            except (ValueError, TypeError):
                postcode_val = str(row['Postcode']) if str(row['Postcode']).isdigit() else ''

        address_parts = [
            str(row['Address']) if pd.notna(row['Address']) else '',
            str(row['Suburb']) if pd.notna(row['Suburb']) else '',
            state,
            postcode_val,
            'Australia'
        ]
        full_address = ', '.join([p for p in address_parts if p])

        print(f"   [{idx + 1}/{len(df_all)}] {city_sheet.replace('_clean', '')} - {row['Name'][:45]}")
        print(f"       📍 {full_address[:70]}")

        # Geocode
        result = geocode_address(geolocator, full_address)

        if result['latitude']:
            print(f"       ✓ ({result['latitude']:.6f}, {result['longitude']:.6f})")
            df_all.at[idx, 'latitude'] = result['latitude']
            df_all.at[idx, 'longitude'] = result['longitude']
            df_all.at[idx, 'geocode_accuracy'] = result['geocode_accuracy']
            df_all.at[idx, 'geocode_source'] = result['geocode_source']
            df_all.at[idx, 'geocode_display_name'] = result['display_name']
            city_stats[city_sheet]['success'] += 1
        else:
            print(f"       ✗ Failed")
            df_all.at[idx, 'geocode_accuracy'] = result['geocode_accuracy']
            failed_count += 1
            city_stats[city_sheet]['failed'] += 1

        print()

    # Save results
    print("\n4. Saving geocoded data...")

    # Save comprehensive CSV
    output_csv = 'All_Services_Geocoded_Complete.csv'
    df_all.to_csv(output_csv, index=False)
    print(f"   ✓ CSV: {output_csv}")

    # Save JSON for web app
    output_json = 'data/all_services_geocoded_complete.json'
    df_json = df_all.to_dict('records')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(df_json, f, indent=2, ensure_ascii=False)
    print(f"   ✓ JSON: {output_json}")

    # Save Excel with all geocoded data
    output_excel = 'Data_final_cleaned_geocoded.xlsx'
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        # Save combined sheet
        df_all.to_excel(writer, sheet_name='All_Cities_Combined', index=False)

        # Save individual city sheets
        for city_sheet in xl.sheet_names:
            city_df = df_all[df_all['City_Sheet'] == city_sheet]
            city_df.to_excel(writer, sheet_name=city_sheet, index=False)

    print(f"   ✓ Excel: {output_excel}")

    # Summary
    total = len(df_all)
    successful = len(df_all[df_all['latitude'].notna()])
    failed = len(df_all[df_all['latitude'].isna()])

    print("\n" + "=" * 70)
    print("📊 GEOCODING SUMMARY")
    print("=" * 70)
    print(f"Total services:        {total}")
    print(f"Successfully geocoded: {successful}")
    print(f"Failed to geocode:     {failed}")
    print(f"Success rate:          {(successful / total * 100):.1f}%")

    # City breakdown
    print("\n📍 Results by city:")
    for city_sheet, stats in city_stats.items():
        city_name = city_sheet.replace('_clean', '')
        success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"   {city_name:15s} {stats['success']:3d}/{stats['total']:3d} geocoded ({success_rate:.0f}%)")

    if failed > 0:
        print(f"\n⚠️  {failed} addresses failed - may need manual review")
        failed_df = df_all[df_all['latitude'].isna()]
        for idx, row in failed_df.iterrows():
            print(f"   - [{row['City_Sheet'].replace('_clean', '')}] {row['Name']}")

    print("\n✅ Geocoding complete!")
    print(f"\n📁 Output files:")
    print(f"   - {output_csv} (185 records, ready for analysis)")
    print(f"   - {output_json} (for web application)")
    print(f"   - {output_excel} (with all sheets + combined)")

if __name__ == '__main__':
    main()
