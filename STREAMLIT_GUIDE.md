# 🚀 Streamlit Frontend Guide

This guide will help you run the **GenAI Governance System Streamlit Frontend** - a beautiful, interactive web application for managing AI governance.

## 📋 Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- **Backend server** running (optional, but recommended)

## 🎯 Quick Start

### Option 1: Using the Startup Script (Recommended)

```bash
# Windows
scripts/start-streamlit.bat

# Linux/Mac
chmod +x scripts/start-streamlit.sh
./scripts/start-streamlit.sh
```

### Option 2: Manual Setup

1. **Install Streamlit** (if not already installed):
   ```bash
   pip install streamlit
   ```

2. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

3. **Start the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

## 🌐 Access Points

Once running, you can access:

- **Streamlit Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000 (if running)
- **API Documentation**: http://localhost:8000/docs (if backend is running)

## 🔧 Running Both Services

### Start Backend First

```bash
# Terminal 1: Start the backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Streamlit Frontend

```bash
# Terminal 2: Start the frontend
cd frontend
streamlit run app.py
```

## 🎮 Features Overview

### 1. **Dashboard**
- Real-time system metrics
- Compliance rate monitoring
- Risk distribution charts
- User activity analytics

### 2. **AI Chat Interface**
- Interactive prompt submission
- Real-time governance processing
- Risk assessment visualization
- Compliance status tracking

### 3. **Audit Logs**
- Comprehensive audit trail
- Search and filter capabilities
- Detailed activity information
- Export functionality

### 4. **Analytics**
- Performance metrics
- Compliance framework tracking
- User behavior analysis
- System health monitoring

### 5. **Policy Management** (Admin Only)
- Governance policy configuration
- Risk threshold settings
- Compliance framework management
- System configuration

### 6. **Feedback System**
- Anonymous feedback collection
- User satisfaction tracking
- System improvement suggestions
- Privacy-protected submissions

## 👤 Demo Credentials

The Streamlit app includes demo authentication:

- **Admin**: `admin` / `admin`
- **Manager**: `manager` / `manager`
- **Analyst**: `analyst` / `analyst`
- **User**: `user` / `user`

## 🎨 UI Features

### Modern Design
- **Responsive layout** that works on all devices
- **Professional color scheme** with blue theme
- **Interactive charts** using Plotly
- **Real-time updates** with live data

### User Experience
- **Intuitive navigation** with sidebar
- **Loading states** for better UX
- **Error handling** with user-friendly messages
- **Toast notifications** for feedback

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
# Backend API URL
BACKEND_URL=http://localhost:8000

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Customization

You can modify the app by editing `frontend/app.py`:

- **Add new pages** by creating new functions
- **Customize styling** by modifying the CSS
- **Add new features** by extending the functionality
- **Integrate with backend** by updating API calls

## 🐛 Troubleshooting

### Common Issues

1. **Port 8501 already in use**:
   ```bash
   # Kill existing process
   taskkill /f /im streamlit.exe  # Windows
   pkill streamlit                 # Linux/Mac
   ```

2. **Backend connection failed**:
   - Ensure backend is running on port 8000
   - Check firewall settings
   - Verify network connectivity

3. **Streamlit not starting**:
   ```bash
   # Reinstall Streamlit
   pip uninstall streamlit
   pip install streamlit
   ```

4. **Missing dependencies**:
   ```bash
   # Install all requirements
   pip install -r requirements.txt
   ```

### Debug Mode

Run Streamlit in debug mode:

```bash
streamlit run app.py --logger.level debug
```

## 📊 Performance Tips

1. **Use caching** for expensive operations
2. **Optimize data loading** with pagination
3. **Implement lazy loading** for large datasets
4. **Use session state** for persistent data

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
```bash
# Build for production
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment
```bash
# Build Docker image
docker build -f Dockerfile.streamlit -t genai-governance-streamlit .

# Run container
docker run -p 8501:8501 genai-governance-streamlit
```

## 📚 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Plotly Charts**: https://plotly.com/python/
- **Pandas DataFrames**: https://pandas.pydata.org/
- **FastAPI Backend**: https://fastapi.tiangolo.com/

## 🎯 Next Steps

1. **Explore the Dashboard** to understand system metrics
2. **Try the AI Chat** to see governance in action
3. **Review Audit Logs** to understand compliance tracking
4. **Check Analytics** for performance insights
5. **Test Policy Management** (if admin user)

## 🆘 Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure backend is running (if using API features)
4. Check network connectivity
5. Review the troubleshooting section above

---

**Happy exploring! 🎉**

The Streamlit frontend provides a beautiful, interactive interface for your GenAI Governance System. Enjoy exploring all the features! 