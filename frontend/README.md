# GenAI Governance Frontend

A beautiful React-based frontend for the GenAI Governance System with real-time monitoring, interactive agent visualization, and comprehensive analytics.

## Features

- 🎨 **Modern UI/UX**: Beautiful, responsive design with Tailwind CSS and Framer Motion
- 📊 **Real-time Dashboard**: Live monitoring with interactive charts and metrics
- 🤖 **Agent Monitor**: Interactive visualization of governance agents
- 📝 **GenAI Process**: Submit prompts with real-time agent processing
- 📈 **Analytics**: Comprehensive analytics and insights
- 📋 **Audit Logs**: Detailed audit trail with search and filtering
- ⚙️ **Settings**: Configurable system settings
- 🔐 **Authentication**: Secure login with role-based access

## Tech Stack

- **React 18** - Modern React with hooks
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Recharts** - Beautiful charts and data visualization
- **React Query** - Data fetching and caching
- **Axios** - HTTP client
- **React Hot Toast** - Toast notifications
- **Heroicons** - Beautiful icons

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend server running on port 8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

### Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/          # Reusable components
│   └── Sidebar.js      # Navigation sidebar
├── hooks/              # Custom React hooks
│   └── useAuth.js      # Authentication hook
├── pages/              # Page components
│   ├── Dashboard.js    # Main dashboard
│   ├── GenAIProcess.js # AI process interface
│   ├── Analytics.js    # Analytics and charts
│   ├── AuditLogs.js    # Audit log viewer
│   ├── AgentMonitor.js # Agent monitoring
│   ├── Settings.js     # System settings
│   └── Login.js        # Authentication
├── App.js              # Main app component
├── index.js            # App entry point
└── index.css           # Global styles
```

## Features Overview

### Dashboard
- Real-time metrics and KPIs
- Interactive charts showing request trends
- Agent performance visualization
- Live system status indicators

### GenAI Process
- Interactive prompt submission
- Real-time agent processing visualization
- Risk assessment and compliance scoring
- Detailed results with recommendations

### Agent Monitor
- Live agent status tracking
- Performance metrics for each agent
- Real-time activity feed
- Interactive agent selection

### Analytics
- Comprehensive data visualization
- Request trends over time
- Compliance distribution charts
- Performance analytics

### Audit Logs
- Searchable audit trail
- Filter by log level and agent
- Detailed activity information
- Export capabilities

### Settings
- System configuration
- Security settings
- User management
- API configuration

## Authentication

The frontend integrates with the backend authentication system:

- **Demo Credentials**:
  - Admin: `admin` / `admin123`
  - User: `user` / `user123`

## API Integration

The frontend communicates with the backend API:

- **Base URL**: `http://localhost:8000`
- **Authentication**: JWT tokens
- **Real-time Updates**: WebSocket connections (planned)

## Styling

The project uses Tailwind CSS with custom configurations:

- **Color Scheme**: Blue/purple gradient theme
- **Typography**: Inter font family
- **Animations**: Framer Motion for smooth transitions
- **Responsive**: Mobile-first design

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Code Style

- ESLint configuration included
- Prettier formatting
- Consistent component structure
- Proper TypeScript-like prop validation

## Deployment

The frontend can be deployed using:

1. **Static Hosting** (Netlify, Vercel, etc.)
2. **Docker** (see main project Dockerfile)
3. **AWS S3 + CloudFront**
4. **Traditional web servers**

## Contributing

1. Follow the existing code style
2. Add proper error handling
3. Include loading states
4. Test on different screen sizes
5. Update documentation as needed

## License

Part of the GenAI Governance System project. 