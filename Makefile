REPO_URL := https://github.com/LolindaLP/spotify-server.git
DB_REPO_URL := https://github.com/LolindaLP/tracksdb.git
PROJECT_DIR := /home/ec2-user/spotify-server
DB_DIR := $(PROJECT_DIR)/tracksdb
PYTHON_VERSION := python3
VENV_DIR := $(PROJECT_DIR)/venv

export CLIENT_ID := your_client_id
export CLIENT_SECRET := your_client_secret

all: install_dependencies clone_repo clone_db setup_env setup_nginx setup_cron start_app test_app

install_dependencies:
        sudo yum update -y
        sudo yum install -y $(PYTHON_VERSION) $(PYTHON_VERSION)-pip nginx git cronie
        sudo systemctl start crond
        sudo systemctl enable crond

clone_repo:
        rm -rf $(PROJECT_DIR)
        git clone $(REPO_URL) $(PROJECT_DIR)

clone_db:
        rm -rf $(DB_DIR)
        git clone $(DB_REPO_URL) $(DB_DIR)
        sudo chown ec2-user:ec2-user $(DB_DIR)/tracks.db
        sudo chmod 644 $(DB_DIR)/tracks.db


setup_env:
        cd $(PROJECT_DIR) && $(PYTHON_VERSION) -m venv $(VENV_DIR)
        cd $(PROJECT_DIR) && $(VENV_DIR)/bin/pip install -r requirements.txt

setup_nginx:
        sudo cp $(PROJECT_DIR)/nginx.conf /etc/nginx/conf.d/myapp.conf
        sudo systemctl restart nginx

setup_cron:
        echo "0 2 * * * /home/ec2-user/spotify-server/run_script.sh" | crontab -
        echo "#!/bin/bash\n\nexport CLIENT_ID=your_client_id\nexport CLIENT_SECRET=your_client_secret\n\n/usr/bin/python3 /home/ec2-us>
        chmod +x /home/ec2-user/spotify-server/run_script.sh

start_app:
        sudo cp $(PROJECT_DIR)/flask_app.service /etc/systemd/system/flask_app.service
        sudo systemctl daemon-reload
        sudo systemctl start flask_app
        sudo systemctl enable flask_app

test_app:
        cd $(PROJECT_DIR) && $(VENV_DIR)/bin/python3 test_app.py

clean:
        rm -rf $(PROJECT_DIR) $(DB_DIR)
        sudo rm /etc/nginx/conf.d/myapp.conf
        sudo systemctl stop flask_app
        sudo systemctl disable flask_app
        sudo rm /etc/systemd/system/flask_app.service
        sudo systemctl daemon-reload
        crontab -r
        rm /home/ec2-user/spotify-server/run_script.sh
