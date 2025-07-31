# Diversifi News Sentiment Analysis API

A FastAPI-based REST API that analyzes sentiment of news headlines for stock symbols. The application fetches news articles for given stock symbols and performs sentiment analysis to provide insights for investment decisions.

## 🚀 Features

- **Real-time News Fetching**: Retrieves latest news articles for any stock symbol
- **AI-Powered Sentiment Analysis**: Uses Google's Gemini AI for accurate sentiment classification
- **Intelligent Caching**: Stores results for 10 minutes to optimize performance
- **RESTful API**: Clean, documented endpoints with automatic validation
- **Docker Support**: Fully containerized for easy deployment
- **Database Integration**: PostgreSQL for persistent data storage

## 📋 Setup Instructions

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Docker (optional, for containerized deployment)
- API keys for EventRegistry and Google Generative AI

### 1. Clone and Setup Environment

```bash
git clone <repository-url>
cd Diversifi
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# For production (minimal dependencies)
pip install -r requirements_minimal.txt

# Or full dependencies (includes development tools)
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
# Database Configuration
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=diversifi

# API Keys
EVENTREGISTRY_API_KEY=your_eventregistry_key
GOOGLE_API_KEY=your_google_ai_key
```

### 5. Database Setup

Ensure PostgreSQL is running and create the database:

```sql
CREATE DATABASE diversifi;
```

The application will automatically create the required tables on startup.

### 6. Run the Application

#### Local Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Docker Deployment
```bash
# Build the image
docker build -t diversifi-app .

# Run the container
docker run -d -p 8000:80 --name diversifi-container \
  -e DB_HOST=host.docker.internal \
  --env-file .env \
  diversifi-app
```

### 7. Access the API

- **API Base URL**: `http://localhost:8000`
- **Interactive Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## 📰 News Data Source

### EventRegistry API

The application uses **EventRegistry** as the primary news data source:

- **Service**: [EventRegistry](https://eventregistry.org/)
- **Why EventRegistry**: 
  - High-quality financial news coverage
  - Concept-based search for better accuracy
  - Real-time news updates
  - Comprehensive company coverage
- **Implementation**: 
  - Fetches 3 most recent articles per stock symbol
  - Uses company concept URIs for precise matching
  - Fallback to keyword search if concept not found
  - Mock data generation for testing when API unavailable

### News Processing Pipeline

1. **Symbol to Concept Mapping**: Convert stock symbol to EventRegistry concept
2. **Article Retrieval**: Fetch latest relevant news articles
3. **Content Extraction**: Extract headlines and relevant text
4. **Fallback Handling**: Use mock data if no articles found

## 🤖 Sentiment Analysis

### Google Generative AI (Gemini)

The application employs **Google's Gemini AI** for sentiment analysis:

- **Model**: `gemini-1.5-flash`
- **Why Gemini**:
  - Fast response times
  - Accurate financial sentiment understanding
  - Cost-effective for production use
  - Reliable API infrastructure

### Sentiment Processing

1. **Primary Method**: Google Gemini AI analysis
2. **Fallback Method**: Keyword-based sentiment analysis
3. **Classification**: Three categories (positive, negative, neutral)
4. **Aggregation**: Overall sentiment based on majority voting


## 🛠 AI Tools Used in Development

### Development Process

1. **GitHub Copilot**: 
   - Code completion and suggestions
   - Error handling implementation
   - API endpoint structure
   - Docker configuration

2. **ChatGPT/Claude**: 
   - Architecture design discussions
   - Error troubleshooting
   - Documentation writing
   - Best practices consultation

3. **AI-Assisted Debugging**:
   - Automated error detection
   - Performance optimization suggestions
   - Security best practices implementation

### Code Quality & Analysis

- **Automated Requirements Analysis**: Used AI to analyze and optimize dependencies (93.5% reduction from 169 to 11 packages)
- **Error Handling**: AI-suggested comprehensive exception handling
- **API Design**: AI-recommended RESTful patterns and response structures

## 📖 API Endpoints

### POST `/news-sentiment`

Analyze sentiment for a stock symbol.

**Request Body:**
```json
{
  "symbol": "AAPL"
}
```

**Response:**
```json
{
  "symbol": "AAPL",
  "timestamp": "2025-07-31T12:00:00",
  "headlines": [
    {
      "title": "Apple reports strong Q3 earnings",
      "sentiment": "positive"
    }
  ],
  "overall_sentiment": "positive"
}
```

### GET `/`

Welcome message and API information.

## 🏗 Architecture

### Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: Google Generative AI, Custom sentiment analysis
- **News API**: EventRegistry
- **Containerization**: Docker
- **Environment**: python-dotenv for configuration

### Project Structure

```
Diversifi/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic and SQLAlchemy models
├── database.py          # Database configuration
├── crud.py              # Database operations
├── news.py              # News fetching logic
├── sentiment.py         # Sentiment analysis
├── requirements_minimal.txt  # Production dependencies
├── requirements.txt     # Full dependencies
├── Dockerfile           # Container configuration
├── .env                 # Environment variables
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DB_USER` | PostgreSQL username | Yes |
| `DB_PASSWORD` | PostgreSQL password | Yes |
| `DB_HOST` | Database host | Yes |
| `DB_PORT` | Database port | Yes |
| `DB_NAME` | Database name | Yes |
| `EVENTREGISTRY_API_KEY` | EventRegistry API key | Yes |
| `GOOGLE_API_KEY` | Google AI API key | Yes |

### Caching Strategy

- **Cache Duration**: 10 minutes per symbol
- **Cache Key**: Stock symbol
- **Purpose**: Reduce API calls and improve response times
- **Implementation**: Database-based caching with timestamp validation

## 🚀 Deployment

### Docker Deployment (Recommended)

```bash
# Build and run
docker build -t diversifi-app .
docker run -d -p 8000:80 --env-file .env diversifi-app
```

### Production Considerations

1. **Database**: Use managed PostgreSQL service
2. **Environment**: Secure environment variable management
3. **Monitoring**: Add logging and health checks
4. **Scaling**: Consider horizontal scaling with load balancer
5. **Security**: Implement API rate limiting and authentication

## 🧪 Testing

### Manual Testing

```bash
# Health check
curl http://localhost:8000/

# Test sentiment analysis
curl -X POST "http://localhost:8000/news-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API testing with Swagger UI.

## 📊 Performance Optimizations

### Dependency Optimization

- **Before**: 169 packages (bloated with unused ML libraries)
- **After**: 11 essential packages (93.5% reduction)
- **Benefit**: Faster Docker builds, smaller images, improved security

### Database Optimization

- **Indexing**: Stock symbol and timestamp fields
- **Caching**: 10-minute cache to reduce external API calls
- **Connection Pooling**: SQLAlchemy connection management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection**: Ensure PostgreSQL is running and credentials are correct
2. **API Keys**: Verify EventRegistry and Google AI API keys are valid
3. **Docker Networking**: Use `host.docker.internal` for database host in containers
4. **Dependencies**: Use `requirements_minimal.txt` for production deployments

### Support

For issues and questions, please check the API documentation at `/docs` or create an issue in the repository.

---

**Built with ❤️ using FastAPI, Google AI, and modern development practices**
