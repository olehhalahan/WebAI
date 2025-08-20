# Setup Guide - Ukrainian Q&A Application

## Prerequisites

### 1. Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, make sure to check "Add Python to PATH"
3. Verify installation: Open Command Prompt and run `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Verify Installation

Open a terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

You should see Python 3.8 or higher.

## Installation Steps

### 1. Clone or Download the Project

If you have Git:
```bash
git clone <repository-url>
cd WebAI
```

Or download and extract the ZIP file.

### 2. Install Dependencies

**Windows:**
```bash
# Open Command Prompt in the project directory
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

### 3. Optional: Set up OpenAI API (for enhanced responses)

1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Copy `config.env.example` to `.env`
3. Add your API key: `OPENAI_API_KEY=your_key_here`

### 4. Run the Application

**Option 1: Using the startup script**
```bash
python run.py
```

**Option 2: Direct execution**
```bash
python app.py
```

**Option 3: Windows batch file**
Double-click `start.bat`

### 5. Access the Application

Open your web browser and go to: `http://localhost:5000`

## Troubleshooting

### Common Issues

**1. "Python not found"**
- Make sure Python is installed and added to PATH
- Try using `python3` instead of `python`

**2. "Module not found" errors**
- Run: `pip install -r requirements.txt`
- Make sure you're in the correct directory

**3. Port already in use**
- Change the port in `app.py` or `run.py`
- Or kill the process using the port

**4. Model loading issues**
- The first run may take longer as models are downloaded
- Check your internet connection
- Ensure you have enough disk space (models are ~100MB)

### System Requirements

- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: At least 500MB free space
- **Internet**: Required for initial model download
- **OS**: Windows 10+, macOS 10.14+, or Linux

### Performance Tips

1. **First Run**: Models will be downloaded (~100MB), be patient
2. **Subsequent Runs**: Much faster as models are cached
3. **Memory Usage**: The application uses ~2-4GB RAM when running
4. **CPU**: Multi-core CPU recommended for better performance

## Alternative: Lightweight Version

If you have issues with the full version, you can use a lightweight version that doesn't require heavy ML dependencies:

```bash
# Install only basic dependencies
pip install flask python-dotenv requests

# Run the lightweight version
python app_lightweight.py
```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are met
3. Check the application logs for error messages
4. Try the lightweight version if the full version doesn't work

## Quick Test

After installation, you can test the application:

```bash
python test_app.py
```

This will run automated tests to verify everything is working correctly.
