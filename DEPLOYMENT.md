# Deployment Guide for Pragmatika Project

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

## Production Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI** (if not installed)
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create pragmatika-project
   ```

4. **Set Python runtime** (optional, Heroku auto-detects)
   ```bash
   heroku buildpacks:set heroku/python
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Open your app**
   ```bash
   heroku open
   ```

### Option 2: Railway

1. **Install Railway CLI** (optional)
   ```bash
   npm i -g @railway/cli
   ```

2. **Login**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

Or use Railway web interface: https://railway.app

### Option 3: Render

1. **Connect GitHub repository** to Render
2. **Create new Web Service**
3. **Settings:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: Python 3

4. **Deploy** (automatic on git push)

### Option 4: Docker

1. **Build Docker image**
   ```bash
   docker build -t pragmatika-app .
   ```

2. **Run container**
   ```bash
   docker run -p 5000:5000 pragmatika-app
   ```

3. **For production with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

### Option 5: DigitalOcean App Platform

1. **Connect GitHub repository**
2. **Create App** from GitHub repo
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn app:app`
4. **Deploy** (automatic)

### Option 6: PythonAnywhere

1. **Upload files** via web interface or git
2. **Configure WSGI file** to point to `app:app`
3. **Reload web app**

## Production Server Setup (VPS/Cloud)

### Using Gunicorn

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app

# Or with more options
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --worker-class sync \
         --timeout 120 \
         --access-logfile - \
         --error-logfile - \
         app:app
```

### Using systemd (Linux)

Create `/etc/systemd/system/pragmatika.service`:

```ini
[Unit]
Description=Pragmatika Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Pragmatika_project
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pragmatika
sudo systemctl start pragmatika
```

### Using Nginx as Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Variables

Create `.env` file for production:

```env
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
```

## Quick Deploy Commands Summary

**Heroku:**
```bash
heroku create && git push heroku main
```

**Railway:**
```bash
railway up
```

**Docker:**
```bash
docker build -t pragmatika . && docker run -p 5000:5000 pragmatika
```

**Local Production:**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```
