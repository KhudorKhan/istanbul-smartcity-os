# DigiBank Frontend

## Overview

The DigiBank frontend is a lightweight, single-page application (SPA) that provides a visualization layer for the Smart City Digital Banking Module. It serves as both a functional demo and GUI mockup for the academic project.

## Purpose

- **Visualization**: Display system behavior, metrics, and transactions
- **Demo**: Functional demonstration of backend API integration
- **Mockup**: GUI representation suitable for academic presentation
- **Monitoring**: Real-time system health and metrics visualization

## Features

### 1. Login & Registration
- User authentication via JWT
- Registration with role selection (Resident/Admin)
- Secure token storage

### 2. Dashboard
- Account balance summary (Fiat & Crypto)
- Recent transactions table
- System health status indicator
- Real-time data from backend

### 3. Payments
- **Fiat Payment Form**: Process traditional currency payments
- **Crypto Payment Form**: Process cryptocurrency payments with network selection
- Service type selection (Parking, Transportation, Utilities, Other)
- Real-time payment processing feedback

### 4. Monitoring (Admin Only)
- System metrics dashboard
- Total transactions and revenue
- System health status
- Audit logs viewer
- Uptime calculation

### 5. Alerts & Notifications
- Transaction-based alerts
- Observer pattern visualization
- Security alert notifications
- Email notification indicators

## Technical Stack

- **Pure HTML/CSS/JavaScript** (No frameworks - lightweight)
- **Vanilla JS** for simplicity and fast loading
- **Font Awesome** icons for UI elements
- **Modern CSS** with CSS variables for theming

## File Structure

```
frontend/
├── index.html              # Main HTML entry point
├── src/
│   ├── app.js             # Main application router
│   ├── styles/
│   │   └── main.css       # Global styles
│   ├── utils/
│   │   ├── config.js      # Configuration (API URLs, endpoints)
│   │   ├── api.js         # API request utilities
│   │   └── auth.js         # Authentication utilities
│   ├── components/
│   │   └── Navbar.js      # Navigation bar component
│   └── pages/
│       ├── Login.js       # Login/Register page
│       ├── Dashboard.js   # Dashboard page
│       ├── Payments.js    # Payment forms
│       ├── Monitoring.js  # Admin monitoring page
│       └── Alerts.js      # Alerts/Notifications page
└── README.md              # This file
```

## Configuration

### Backend URL Setup

Edit `src/utils/config.js` to set your backend API URL:

```javascript
API_BASE_URL: 'https://your-render-app.onrender.com'
```

For local development:
```javascript
API_BASE_URL: 'http://localhost:8080'
```

## Running the Frontend

### Option 1: Simple HTTP Server (Recommended)

```bash
# Python 3
python -m http.server 3000

# Node.js (if you have http-server installed)
npx http-server -p 3000

# Then open: http://localhost:3000
```

### Option 2: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"

### Option 3: Serve from Backend (Optional)

You can configure Spring Boot to serve static files, but for this project, keeping them separate is recommended.

## API Integration

The frontend integrates with the following backend endpoints:

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/account/balance` - Get account balance
- `POST /api/pay/fiat` - Process fiat payment
- `POST /api/pay/crypto` - Process crypto payment
- `GET /api/transactions` - Get transaction history
- `GET /api/metrics` - Get system metrics (Admin)
- `GET /api/metrics/logs` - Get audit logs (Admin)
- `GET /actuator/health` - System health check

## Authentication

- JWT tokens are stored in `localStorage`
- Tokens are sent in `Authorization: Bearer {token}` header
- Automatic redirect to login if token is missing or invalid

## Design Patterns Visualization

The frontend demonstrates the following design patterns through UI:

1. **Observer Pattern**: Alerts page shows notification system in action
2. **Adapter Pattern**: Crypto payment form shows multiple network adapters
3. **Command Pattern**: Payment forms execute payment commands
4. **Singleton Pattern**: Monitoring page shows CityController metrics
5. **Template Method**: Security checks are transparent in payment flow

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Edge, Safari)
- ES6+ JavaScript features required
- Fetch API for HTTP requests

## Screenshots

Screenshots should be captured for:
- Login page
- Dashboard with data
- Payment forms
- Monitoring page (Admin)
- Alerts page

Save screenshots to `docs/screenshots/` directory.

## Notes

- This is a **demo/mockup** frontend, not production-ready
- No build process required - pure static files
- CORS must be enabled on backend (already configured)
- Environment-based API URL for flexibility
- Lightweight design emphasizes clarity over features

## Future Enhancements (Optional)

- Real-time WebSocket updates
- Chart visualizations for metrics
- Export functionality for transactions
- Advanced filtering and search
- Responsive mobile optimization

