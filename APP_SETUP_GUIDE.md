# Integrative Oncology Services Finder - Setup Guide

## Quick Start

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Code editor (VS Code recommended)

### Step 1: Create Next.js Application

```bash
# Navigate to your project directory
cd /Users/afzalkhan/Academic-projects/paper-4-cancer-oncology

# Create Next.js app
npx create-next-app@latest oncology-finder

# Options to select:
# ✔ Would you like to use TypeScript? Yes
# ✔ Would you like to use ESLint? Yes
# ✔ Would you like to use Tailwind CSS? Yes
# ✔ Would you like to use `src/` directory? No
# ✔ Would you like to use App Router? Yes
# ✔ Would you like to customize the default import alias? No

cd oncology-finder
```

### Step 2: Install Dependencies

```bash
# Map and routing libraries
npm install leaflet react-leaflet
npm install -D @types/leaflet

# UI components and utilities
npm install lucide-react
npm install clsx tailwind-merge

# Distance calculations
npm install geolib

# Data fetching
npm install swr
```

### Step 3: Project Structure

```
oncology-finder/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page with map
│   ├── services/
│   │   └── [id]/page.tsx       # Service detail page
│   ├── about/page.tsx          # About page
│   └── api/
│       ├── services/route.ts   # Services API
│       └── route/route.ts      # Routing API
├── components/
│   ├── map/
│   │   ├── MapView.tsx         # Main map component
│   │   ├── ServiceMarker.tsx   # Individual markers
│   │   └── RouteLayer.tsx      # Route visualization
│   ├── search/
│   │   ├── SearchBar.tsx       # Search input
│   │   ├── LocationButton.tsx  # Geolocation
│   │   └── FilterPanel.tsx     # Filters
│   ├── service/
│   │   ├── ServiceCard.tsx     # Service card
│   │   └── ServiceDetail.tsx   # Detail view
│   └── ui/                     # Reusable components
├── lib/
│   ├── services.ts             # Service data utilities
│   ├── geocoding.ts            # Geocoding functions
│   ├── routing.ts              # Routing calculations
│   └── utils.ts                # Helper functions
├── public/
│   └── data/
│       └── services.json       # Service data
└── styles/
    └── globals.css             # Global styles
```

### Step 4: Copy Data Files

```bash
# From your project root, copy geocoded data
mkdir -p oncology-finder/public/data
cp data/services_geocoded.json oncology-finder/public/data/services.json
```

### Step 5: Configure Leaflet CSS

Add to `app/layout.tsx`:

```tsx
import 'leaflet/dist/leaflet.css'
```

### Step 6: Start Development Server

```bash
npm run dev
# Open http://localhost:3000
```

## Key Files to Create

### 1. `lib/services.ts` - Service Data Utilities

```typescript
import servicesData from '@/public/data/services.json'

export interface Service {
  Name: string
  Organization: string
  'Provider Type': string
  'Facility Type': string
  Address: string
  Suburb: string
  Postcode: number
  Phone: string
  Website: string
  group_services_standardized: string
  individual_services_standardized: string
  associated_services_standardized: string
  'Verification Notes (as of Oct 2025)': string
  latitude: number
  longitude: number
  geocode_accuracy: string
  geocode_source: string
  geocode_display_name: string
}

export function getAllServices(): Service[] {
  return servicesData as Service[]
}

export function getServiceById(id: string): Service | undefined {
  const services = getAllServices()
  const index = parseInt(id)
  return services[index]
}

export function getServiceTypes(): string[] {
  const services = getAllServices()
  const types = new Set<string>()

  services.forEach(service => {
    const groupServices = service.group_services_standardized
    if (groupServices && groupServices !== 'none') {
      groupServices.split(';').forEach(type => {
        types.add(type.trim())
      })
    }
  })

  return Array.from(types).sort()
}

export function getProviderTypes(): string[] {
  const services = getAllServices()
  const types = new Set(services.map(s => s['Provider Type']))
  return Array.from(types).sort()
}
```

### 2. `lib/distance.ts` - Distance Calculations

```typescript
import { getDistance } from 'geolib'

export interface Coordinates {
  latitude: number
  longitude: number
}

export function calculateDistance(
  from: Coordinates,
  to: Coordinates
): number {
  return getDistance(
    { lat: from.latitude, lon: from.longitude },
    { lat: to.latitude, lon: to.longitude }
  )
}

export function formatDistance(meters: number): string {
  if (meters < 1000) {
    return `${meters}m`
  }
  return `${(meters / 1000).toFixed(1)}km`
}

export function sortByDistance(
  services: any[],
  userLocation: Coordinates
): any[] {
  return services
    .map(service => ({
      ...service,
      distance: calculateDistance(userLocation, {
        latitude: service.latitude,
        longitude: service.longitude
      })
    }))
    .sort((a, b) => a.distance - b.distance)
}
```

### 3. `components/map/MapView.tsx` - Main Map Component

```typescript
'use client'

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { Service } from '@/lib/services'

// Fix for default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: '/leaflet/marker-icon-2x.png',
  iconUrl: '/leaflet/marker-icon.png',
  shadowUrl: '/leaflet/marker-shadow.png',
})

interface MapViewProps {
  services: Service[]
  center?: [number, number]
  zoom?: number
}

export default function MapView({
  services,
  center = [-34.9285, 138.6007], // Adelaide
  zoom = 11
}: MapViewProps) {
  return (
    <MapContainer
      center={center}
      zoom={zoom}
      style={{ height: '100%', width: '100%' }}
      className="z-0"
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {services.map((service, index) => (
        <Marker
          key={index}
          position={[service.latitude, service.longitude]}
        >
          <Popup>
            <div className="p-2">
              <h3 className="font-bold text-sm">{service.Name}</h3>
              <p className="text-xs text-gray-600">{service.Organization}</p>
              <p className="text-xs mt-1">{service['Provider Type']}</p>
              <a
                href={`/services/${index}`}
                className="text-blue-600 text-xs hover:underline block mt-2"
              >
                View Details →
              </a>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  )
}
```

### 4. `app/page.tsx` - Home Page

```typescript
'use client'

import dynamic from 'next/dynamic'
import { getAllServices } from '@/lib/services'
import { useState } from 'react'

// Dynamic import to avoid SSR issues with Leaflet
const MapView = dynamic(() => import('@/components/map/MapView'), {
  ssr: false,
  loading: () => <div className="h-full flex items-center justify-center">Loading map...</div>
})

export default function Home() {
  const services = getAllServices()
  const [selectedService, setSelectedService] = useState<any>(null)

  return (
    <main className="h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-lg z-10">
        <h1 className="text-2xl font-bold">Integrative Oncology Services Finder</h1>
        <p className="text-sm opacity-90">Find support services near you</p>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Service List Sidebar */}
        <aside className="w-96 overflow-y-auto bg-gray-50 border-r">
          <div className="p-4">
            <h2 className="font-bold text-lg mb-4">
              {services.length} Services Found
            </h2>
            <div className="space-y-3">
              {services.map((service, index) => (
                <div
                  key={index}
                  className="bg-white p-3 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => setSelectedService(service)}
                >
                  <h3 className="font-semibold text-sm">{service.Name}</h3>
                  <p className="text-xs text-gray-600">{service.Organization}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {service['Provider Type']}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </aside>

        {/* Map */}
        <div className="flex-1">
          <MapView services={services} />
        </div>
      </div>
    </main>
  )
}
```

## Next Steps

1. ✅ **Data is geocoded** - All 25 services have coordinates
2. **Create the app** - Follow steps above
3. **Customize UI** - Match your branding
4. **Add features**:
   - Search functionality
   - Filters by service type
   - Routing with OpenRouteService
   - Mobile responsive design
5. **Deploy** - Deploy to Vercel

## Resources

- **Next.js Docs**: https://nextjs.org/docs
- **React Leaflet**: https://react-leaflet.js.org/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **OpenRouteService**: https://openrouteservice.org/

## Troubleshooting

### Leaflet Icons Not Showing

Copy marker images to `public/leaflet/`:
```bash
mkdir -p public/leaflet
# Download from: https://github.com/Leaflet/Leaflet/tree/main/dist/images
```

### Map Not Rendering

Make sure to use dynamic import with `ssr: false` for map components.

### TypeScript Errors

Install type definitions:
```bash
npm install -D @types/leaflet @types/geojson
```

---

**Ready to code?** Follow the steps above and you'll have a working map application in about 30 minutes!
