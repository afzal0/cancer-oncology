# Integrative Oncology Services Finder - Application Plan

## Executive Summary

Building a user-friendly web application to help cancer patients, survivors, and caregivers find nearby integrative oncology services with interactive maps, routing, and detailed service information.

## Application Features

### Core Features
1. **Interactive Map View**
   - Display all services as markers on an OpenStreetMap-based interface
   - Cluster markers for better performance and UX
   - Click markers to view service details
   - Filter by service types (yoga, meditation, support groups, etc.)

2. **Search & Discovery**
   - Search by current location (geolocation)
   - Search by address/suburb/postcode
   - Find nearest services within specified radius
   - Sort by distance

3. **Routing & Directions**
   - Calculate driving directions (distance, time, route)
   - Calculate walking directions
   - Visual route display on map
   - Turn-by-turn directions

4. **Service Information**
   - Detailed service cards with all information
   - Contact details (phone, website)
   - Available programs (group/individual services)
   - Provider type and facility information
   - Verification status

5. **Filtering & Sorting**
   - Filter by provider type (hospital, NGO, etc.)
   - Filter by service types (yoga, meditation, exercise, etc.)
   - Filter by city/suburb
   - Sort by distance, name, or provider type

### Advanced Features (Phase 2)
- Save favorite services
- Share services via link
- Print directions
- Mobile-responsive design
- Accessibility features (WCAG 2.1 AA)
- Service availability calendar
- User reviews and ratings

## Technology Stack

### Frontend
- **Framework**: React with Next.js 14+ (App Router)
  - Server-side rendering for better SEO
  - Static generation for performance
  - API routes for backend functionality

- **Mapping**: Leaflet.js with React-Leaflet
  - Open-source, lightweight
  - Extensive plugin ecosystem
  - Works seamlessly with OSM tiles

- **UI Library**:
  - Tailwind CSS for styling
  - shadcn/ui for component library
  - Lucide React for icons

- **State Management**:
  - React Context API or Zustand
  - React Query for data fetching

### Mapping & Routing
- **Map Tiles**: OpenStreetMap (OSM)
  - Free and open-source
  - Multiple tile providers (OpenStreetMap, Mapbox, etc.)

- **Geocoding**: Nominatim (OSM Geocoding API)
  - Free geocoding service
  - Reverse geocoding support

- **Routing**: OpenRouteService or OSRM
  - Free routing API
  - Supports driving, walking, cycling
  - Turn-by-turn directions
  - Distance and duration calculations

### Data & Backend
- **Database**: JSON files for initial version (185 records)
  - Upgrade to PostgreSQL + PostGIS for production

- **API**: Next.js API routes
  - Serverless functions
  - Easy deployment

### Deployment
- **Hosting**: Vercel (free tier)
  - Seamless Next.js integration
  - Automatic deployments
  - Edge functions
  - Custom domain support

- **CDN**: Vercel Edge Network
- **Analytics**: Vercel Analytics (optional)

## Application Architecture

```
integrative-oncology-finder/
├── app/                          # Next.js 14 App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page with map
│   ├── services/                # Service pages
│   │   └── [id]/page.tsx       # Individual service detail
│   ├── about/page.tsx           # About the dataset
│   └── api/                     # API routes
│       ├── services/route.ts    # Get all services
│       ├── geocode/route.ts     # Geocoding endpoint
│       └── route/route.ts       # Routing calculations
├── components/
│   ├── Map/
│   │   ├── MapView.tsx          # Main map component
│   │   ├── ServiceMarker.tsx    # Service marker
│   │   ├── MarkerCluster.tsx    # Clustering
│   │   └── RouteLayer.tsx       # Route visualization
│   ├── Search/
│   │   ├── SearchBar.tsx        # Search input
│   │   ├── LocationSearch.tsx   # Geolocation
│   │   └── FilterPanel.tsx      # Filters
│   ├── Service/
│   │   ├── ServiceCard.tsx      # Service info card
│   │   ├── ServiceList.tsx      # List view
│   │   └── ServiceDetail.tsx    # Detailed view
│   └── UI/                      # Reusable UI components
├── lib/
│   ├── geocoding.ts             # Geocoding utilities
│   ├── routing.ts               # Routing calculations
│   ├── distance.ts              # Distance calculations
│   └── filters.ts               # Filter logic
├── data/
│   └── services-geocoded.json   # Geocoded dataset
├── public/
│   └── icons/                   # Custom map markers
└── styles/
    └── globals.css              # Global styles
```

## Implementation Phases

### Phase 1: Foundation (Week 1)
1. **Data Preparation**
   - Geocode all 185 addresses
   - Add latitude/longitude to dataset
   - Validate coordinates
   - Export as JSON

2. **Project Setup**
   - Initialize Next.js project
   - Install dependencies (Leaflet, Tailwind, etc.)
   - Set up project structure
   - Configure TypeScript

3. **Basic Map Implementation**
   - Integrate Leaflet with OSM tiles
   - Display all services as markers
   - Implement marker clustering
   - Add popup with basic info

### Phase 2: Search & Discovery (Week 2)
1. **Search Functionality**
   - Implement address search
   - Add geolocation support
   - Create search bar UI
   - Display search results

2. **Distance Calculations**
   - Calculate distance from user location
   - Sort services by distance
   - Show distance on service cards
   - Filter by radius

3. **Filtering System**
   - Service type filters
   - Provider type filters
   - City/suburb filters
   - Multi-select functionality

### Phase 3: Routing & Directions (Week 3)
1. **Routing Integration**
   - Integrate OpenRouteService API
   - Calculate driving routes
   - Calculate walking routes
   - Display routes on map

2. **Directions UI**
   - Turn-by-turn directions
   - Route summary (distance, time)
   - Route options (fastest, shortest)
   - Print directions

### Phase 4: UI/UX Polish (Week 4)
1. **Responsive Design**
   - Mobile optimization
   - Tablet layouts
   - Desktop layouts
   - Touch-friendly controls

2. **Service Details**
   - Detailed service pages
   - Contact information
   - Available programs
   - Opening hours (if available)

3. **Performance Optimization**
   - Code splitting
   - Image optimization
   - Lazy loading
   - Caching strategies

### Phase 5: Deployment & Testing (Week 5)
1. **Testing**
   - Cross-browser testing
   - Mobile device testing
   - Accessibility testing
   - Performance testing

2. **Deployment**
   - Deploy to Vercel
   - Set up custom domain
   - Configure analytics
   - Set up monitoring

3. **Documentation**
   - User guide
   - Developer documentation
   - API documentation
   - Deployment guide

## UI/UX Design Guidelines

### Design Principles
- **Clean & Minimal**: Focus on the map and services
- **Accessible**: WCAG 2.1 AA compliance
- **Fast**: Optimize for performance
- **Intuitive**: Clear navigation and actions
- **Mobile-First**: Design for mobile, enhance for desktop

### Color Scheme
- Primary: Blue (#2c5aa0) - matches website
- Secondary: Green (#27ae60) - for actions
- Accent: Light blue (#4a90e2)
- Neutral: Grays for text and backgrounds
- Success: Green for confirmed services
- Warning: Orange for unverified info

### Layout
```
┌─────────────────────────────────────────┐
│ Header (Logo, Search Bar, Filters)     │
├─────────────────┬───────────────────────┤
│                 │                       │
│   Service List  │      Map View         │
│   (Scrollable)  │   (Interactive)       │
│                 │                       │
│   [Card 1]      │   ╔═══╗              │
│   [Card 2]      │   ║ M ║ Markers      │
│   [Card 3]      │   ╚═══╝              │
│   ...           │    Routes & Clusters  │
│                 │                       │
└─────────────────┴───────────────────────┘
│              Footer                     │
└─────────────────────────────────────────┘
```

### Service Card Design
```
┌─────────────────────────────────┐
│ ⚕️ Cancer Services (RAH)       │
│ Royal Adelaide Hospital         │
│ ─────────────────────────────── │
│ 📍 1.2 km away                  │
│ 🏥 Public Hospital              │
│                                 │
│ Services: Yoga, Meditation,     │
│ Exercise, Support Group         │
│                                 │
│ [📞 Call] [🗺️ Directions] [ℹ️] │
└─────────────────────────────────┘
```

## Data Requirements

### Geocoding Requirements
All addresses need to be geocoded to latitude/longitude coordinates:

**Required Fields:**
- `latitude`: Decimal degrees
- `longitude`: Decimal degrees
- `geocode_accuracy`: Quality indicator
- `geocode_source`: Source API used

**Address Format:**
- Combine: Address, Suburb, State, Postcode, Australia
- Example: "Port Rd, Adelaide SA 5000, Australia"

## API Integrations

### 1. Nominatim (Geocoding)
- **Endpoint**: https://nominatim.openstreetmap.org/search
- **Rate Limit**: 1 request/second
- **Cost**: Free
- **Usage**: Convert addresses to coordinates

### 2. OpenRouteService (Routing)
- **Endpoint**: https://api.openrouteservice.org/v2/directions
- **Rate Limit**: 2000 requests/day (free tier)
- **Cost**: Free tier available
- **Usage**: Calculate routes and directions

### 3. OSM Tiles (Map Display)
- **Tile Server**: https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
- **Rate Limit**: Reasonable use
- **Cost**: Free
- **Usage**: Display map tiles

## Development Timeline

### Week 1: Foundation & Geocoding
- Days 1-2: Geocode all addresses
- Days 3-4: Set up Next.js project
- Days 5-7: Basic map with markers

### Week 2: Search & Filters
- Days 1-3: Search functionality
- Days 4-5: Distance calculations
- Days 6-7: Filter system

### Week 3: Routing
- Days 1-4: Route integration
- Days 5-7: Directions UI

### Week 4: Polish
- Days 1-3: Responsive design
- Days 4-5: Service details
- Days 6-7: Performance optimization

### Week 5: Launch
- Days 1-3: Testing
- Days 4-5: Deployment
- Days 6-7: Documentation

## Success Metrics

### Technical Metrics
- Page load time < 2 seconds
- Map interaction lag < 100ms
- Mobile performance score > 90
- Accessibility score > 95

### User Metrics
- Time to find nearest service < 30 seconds
- User engagement > 2 minutes average
- Bounce rate < 40%
- Mobile users > 60%

## Future Enhancements

### Phase 2 Features
- User accounts and saved services
- Service booking/appointments
- Real-time availability
- User reviews and ratings
- Multilingual support
- Service recommendations based on needs

### Advanced Features
- Integration with health records
- Telehealth service information
- Community forums
- Event calendar for group programs
- Push notifications for new services

## Resources & Tools

### Development Tools
- **Code Editor**: VS Code
- **Version Control**: Git + GitHub
- **Package Manager**: npm or yarn
- **Testing**: Jest + React Testing Library

### Design Tools
- **Prototyping**: Figma
- **Icons**: Lucide Icons
- **Images**: Unsplash (free stock photos)

### Documentation
- **React Leaflet**: https://react-leaflet.js.org/
- **Next.js**: https://nextjs.org/docs
- **OpenRouteService**: https://openrouteservice.org/dev/
- **Nominatim**: https://nominatim.org/release-docs/latest/

## Cost Analysis

### Development Costs
- **Hosting**: $0 (Vercel free tier)
- **APIs**: $0 (free tiers sufficient for initial launch)
- **Domain**: ~$12/year (optional)
- **Development**: In-house

### Operational Costs
- **Hosting**: $0-20/month (scales with traffic)
- **API Calls**: $0-50/month (after free tier)
- **Monitoring**: $0 (Vercel analytics)
- **Total**: $0-70/month

## Next Steps

1. ✅ Review and approve this plan
2. 🔄 Geocode all addresses in dataset
3. 📦 Set up development environment
4. 💻 Start Phase 1 implementation
5. 🎨 Create UI mockups
6. 🚀 Begin development sprints

---

**Ready to Start?** Let's begin with geocoding the addresses and setting up the project structure!
