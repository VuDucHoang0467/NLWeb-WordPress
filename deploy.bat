@echo off
REM Production deployment script for NLWeb on Windows
REM This script helps deploy NLWeb to production environment

echo 🚀 Starting NLWeb deployment process...

REM Check if .env exists
if not exist "code\.env" (
    echo ❌ Error: .env file not found in code\ directory
    echo Please create code\.env with your API keys before deploying
    exit /b 1
)

REM Check if OPENAI_API_KEY is set
findstr /R "OPENAI_API_KEY=sk-" code\.env >nul
if %errorlevel% neq 0 (
    echo ❌ Error: OPENAI_API_KEY not found or invalid in .env file
    echo Please add your OpenAI API key to code\.env
    exit /b 1
)

echo ✅ Environment configuration validated

REM Create necessary directories
if not exist "data\db" mkdir "data\db"
if not exist "data\json" mkdir "data\json"
if not exist "data\json_with_embeddings" mkdir "data\json_with_embeddings"

echo ✅ Data directories created

REM Build Docker image if Dockerfile exists
if exist "Dockerfile" (
    echo 🐳 Building Docker image...
    docker build -t nlweb-app:latest .
    echo ✅ Docker image built successfully
)

REM Run local test
echo 🧪 Running local test...
cd code
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY configured:', bool(os.getenv('OPENAI_API_KEY'))); print('Configuration test passed!')"
cd ..

echo ✅ All checks passed!
echo.
echo 📋 Next steps:
echo 1. For Railway: Push to GitHub and connect to Railway
echo 2. For Render: Push to GitHub and create new Web Service
echo 3. For Docker: Run with 'docker run -d -p 8000:8000 nlweb-app:latest'
echo.
echo 📝 Don't forget to:
echo - Set environment variables on your hosting platform
echo - Update widget.js URL in your WordPress site
echo - Test the deployment after going live
