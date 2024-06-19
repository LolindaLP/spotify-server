# Spotify Top 50 Songs

http://ec2-52-59-172-131.eu-central-1.compute.amazonaws.com/

## Project Overview

<p style="font-size: 18px;">The Flask web application displays today's top 50 Spotify tracks and allows users to view top tracks for other days in the database. It also features a graph showing the top 5 most popular artists and their song counts per day.</p>

## How It Works

### 1. Daily Data Acquisition:
<p style="font-size: 16px;">
- A cron job runs a Python script daily to generate a Spotify API access token.
- The script fetches the Spotify Top 50 Global playlist data.
- Track details (title, artist, album, popularity) are extracted and stored in an SQLite database.
</p>

### 2. Data Storage:
<p style="font-size: 16px;">
- Track data is stored in an SQLite database, maintaining historical data for user access.
</p>

### 3. Flask Web Interface:
<p style="font-size: 16px;">
- The Flask app retrieves and displays the top 50 tracks for the current day.
- It uses the Plotly library to create a graph of the top 5 artists and their song contributions.
- Users can select different dates to view past top tracks, dynamically updating the displayed data.
</p>

### 4. User Interaction:
<p style="font-size: 16px;">
- A date picker allows users to choose specific dates.
- The application fetches and displays data for the selected date from the database.
</p>

### 5. Data Persistence:
<p style="font-size: 16px;">
- The SQLite database ensures data persistence for future access.
- Daily cron jobs update the database with the latest top 50 tracks.
</p>

## Setup Instructions

<p style="font-size: 18px;">
Follow these steps to set up the project from the <a href="https://github.com/LolindaLP/spotify-server">repository</a>:
</p>

### 1. Install Python:
<p style="font-size: 16px;">
On Ubuntu/Debian-based systems:
</p>

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```
### 2. Clone the Repository:
  
```bash
git clone https://github.com/LolindaLP/spotify-server.git
cd spotify-server
```

### 3. Create and Activate a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies:
  
```bash
pip install -r requirements.txt
```

### 5. Add Your Secrets:
<p style="font-size: 16px;">
Create a secrets in Github Actions:
</p>

```bash
- EC2_SSH_KEY
- HOST_DNS
- TARGET_DIR
- USERNAME
```

### 6. Download last version of data base:
<p style="font-size: 16px;">
Clone git repository with last version of data base
</p>

```bash
git clone git@github.com:LolindaLP/tracksdb.git
```

### 7. Set Up Cron Job:
<p style="font-size: 16px;">
To set up a cron job that runs the update_spotify_data.py script daily and logs the execution time, follow these steps:

Open the cron table for editing:
</p>

```bash
crontab -e
0 2 * * * echo run_script.sh 
```
<p style="font-size: 16px;">
Add content for run_script.sh:
</p>

```bash
#!/bin/bash

export CLIENT_ID= your_client_id
export CLIENT_SECRET= your_client_secret

/usr/bin/python3 /path/to/data_base.py
```

<p style="font-size: 16px;">
This concise overview captures the essential details and steps for setting up and understanding the project.
</p>


### 8. Set Up Nginx:
<p style="font-size: 16px;">
</p>

```bash
sudo apt install nginx

cd /ect/nginx/sites-enabled/
sudo nano fastapi_nginx

server {
  listen 80;
  server_name server_name;
  location / {
    proxy_pass http://127.0.0.1:8000;
  }
}
sudo service nginx restart
```


### 9. Set Up Systemd Fastapi:
<p style="font-size: 16px;">

</p>

```bash
cd /etc/systemd/system/
sudo nano flask_app.service 

Description=Flask App
After=network.target
[Service]
User=YOUR_||USERNAME|
WorkingDirectory=YOUR WORKING
ExecStart=/home/ec2-user/venv/bin/gunicorn -b localhost:5000 app:app
Restart=always
[Install]
WantedBy=multi-user.target

sudo service flask_app start
```
