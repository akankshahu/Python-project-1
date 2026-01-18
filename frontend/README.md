# DataMAx Frontend

Angular-based web interface for the DataMAx pharmaceutical data analytics platform.

## Prerequisites

- Node.js 16+ and npm
- Angular CLI 16+

## Installation

```bash
# Install dependencies
npm install

# Install Angular CLI globally (if not already installed)
npm install -g @angular/cli
```

## Development

```bash
# Start development server
npm start
# or
ng serve

# Open browser at http://localhost:4200
```

## Build

```bash
# Build for production
npm run build

# Output will be in dist/ directory
```

## Features

- **Dashboard**: Analytics overview with key metrics
- **Drugs List**: Browse pharmaceutical drugs
- **Clinical Trials**: View and filter clinical trials
- **Responsive Design**: Mobile-friendly interface

## API Configuration

Update the API URL in `src/environments/environment.ts`:

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000/api/v1'
};
```

## Project Structure

```
src/
├── app/
│   ├── components/       # UI components
│   ├── services/         # API services
│   ├── models/           # TypeScript interfaces
│   ├── app.component.ts  # Root component
│   └── app.routes.ts     # Routing configuration
├── environments/         # Environment configs
├── assets/              # Static assets
└── styles.css           # Global styles
```
