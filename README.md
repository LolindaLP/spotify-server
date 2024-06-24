# Spotify Top 50 Songs

https://tgs50.com/

## Project Overview

<p style="font-size: 18px;">The Flask web application displays today's top 50 Spotify tracks and allows users to view top tracks for other days in the database. It also features a graph showing the top 5 most popular artists and their song counts per day.</p>

## How It Works

### 1. Daily Data Acquisition:
<p style="font-size: 16px;">
<br>- A cron job runs a Python script daily to generate a Spotify API access token.
<br>- The script fetches the Spotify Top 50 Global playlist data.
<br>- Track details (title, artist, album, popularity) are extracted and stored in an SQLite database.
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

### 1. Create Your EC2 Instance:
<p style="font-size: 16px;">
1. Launch an EC2 Instance:
  <p style="font-size: 14px;">
  - Go to the AWS Management Console.
  - Navigate to the EC2 Dashboard.
  - Click on "Launch Instance".
  - Select an Amazon Machine Image (AMI) (e.g., Amazon Linux 2).
  - Choose an instance type (e.g., t2.micro).
  - Configure instance details and add storage as needed.
  - Configure the security group to allow SSH (port 22).
  - Review and launch the instance.
  </p>
</p>

### 2. Install make:
<p style="font-size: 16px;">
Install and start makefile:
</p>

```bash
sudo yum install make
make
```

<p style="font-size: 16px;">
This concise overview captures the essential details and steps for setting up and understanding the project.
</p>
