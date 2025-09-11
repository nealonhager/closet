# Closet AI - Smart Wardrobe Management

A full-stack application that uses AI to extract and organize clothing items from photos, helping you build a digital wardrobe.

## 🚀 Features

- **AI-Powered Image Processing**: Uses Google's Gemini AI to extract clothing items from photos
- **Modern React Frontend**: Built with React 18, Vite, TypeScript, and Tailwind CSS
- **RESTful API**: Flask-based backend with comprehensive endpoints
- **Dockerized**: Complete containerization for easy deployment
- **Responsive UI**: Beautiful, mobile-friendly interface with Untitled UI components
- **File Management**: Upload, process, and download processed images

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │   Flask API     │    │   Google AI     │
│   (Port 3000)   │◄──►│   (Port 5000)   │◄──►│   (Gemini)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **Headless UI** for accessible components
- **Heroicons** for icons

### Backend
- **Flask** with Python 3.12
- **Google Gemini AI** for image processing
- **Pillow** for image manipulation
- **Gunicorn** for production serving

### Infrastructure
- **Docker** & **Docker Compose**
- **Nginx** for reverse proxy and static file serving
- **Multi-stage builds** for optimized images

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Google AI API key (for Gemini)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd closet
```

### 2. Set up Google AI API Key
```bash
# Set your API key (replace with your actual key)
export GOOGLE_API_KEY="your_api_key_here"
```

### 3. Run with Docker Compose
```bash
# Production mode
docker-compose up --build

# Development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up --build
```

### 4. Access the Application
- **Frontend**: http://localhost:3001
- **API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/health

## 📱 Usage

1. **Upload an Image**: Drag and drop or click to select a clothing photo
2. **Specify Article Type**: Enter what type of clothing it is (e.g., "sweater", "dress")
3. **Process**: Click "Process Image" to extract the clothing item
4. **View Results**: See your processed images in the gallery
5. **Download**: Download individual processed images

## 🔧 API Endpoints

### Health Check
```bash
GET /health
```

### Process Image
```bash
POST /process
Content-Type: multipart/form-data

Form data:
- file: Image file (PNG, JPG, JPEG)
- article: Clothing type (string)
```

### List Processed Files
```bash
GET /list-processed
```

### Download File
```bash
GET /download/<filename>
```

## 🐳 Docker Commands

### Production
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Development
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Rebuild specific service
docker-compose build closet-frontend
```

### Individual Services
```bash
# Build frontend only
docker build -t closet-frontend ./frontend

# Build backend only
docker build -t closet-api .

# Run frontend
docker run -p 3001:80 closet-frontend

# Run backend
docker run -p 5000:5000 -v $(pwd)/images:/app/images closet-api
```

## 📁 Project Structure

```
closet/
├── app.py                 # Flask API server
├── requirements.txt       # Python dependencies
├── Dockerfile            # Backend Docker image
├── docker-compose.yml    # Production orchestration
├── docker-compose.dev.yml # Development orchestration
├── images/               # Image storage
│   ├── input/           # Uploaded images
│   ├── output/          # Processed images
│   └── archive/         # Archived images
└── frontend/            # React application
    ├── src/
    │   ├── components/  # React components
    │   ├── utils/      # Utility functions
    │   └── App.tsx     # Main app component
    ├── public/         # Static assets
    ├── package.json    # Node dependencies
    ├── Dockerfile      # Frontend Docker image
    └── nginx.conf      # Nginx configuration
```

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

## 🚀 Deployment

### Production Deployment
1. Set up your Google AI API key
2. Configure environment variables
3. Run `docker-compose up -d`
4. Set up reverse proxy (nginx) if needed
5. Configure SSL certificates

### Environment Variables
- `GOOGLE_API_KEY`: Your Google AI API key
- `FLASK_ENV`: Set to `production` for production mode

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**API Connection Issues**
- Check if the backend is running on port 5000
- Verify the API proxy configuration in `frontend/vite.config.ts`

**Image Processing Fails**
- Ensure your Google AI API key is set correctly
- Check the API logs: `docker-compose logs closet-api`

**Frontend Not Loading**
- Check if the frontend container is running
- Verify port 3001 is not in use by another service

**File Upload Issues**
- Check file size (max 16MB)
- Ensure file type is supported (PNG, JPG, JPEG)

### Debug Commands
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f closet-api
docker-compose logs -f closet-frontend

# Access container shell
docker-compose exec closet-api bash
docker-compose exec closet-frontend sh
```