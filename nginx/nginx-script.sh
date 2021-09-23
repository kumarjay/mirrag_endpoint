echo 'Hello World'

sudo apt update
sudo apt install nginx

sudo rm /etc/nginx/sites-enabled/default
sudo touch flask-front
sudo cp nginx_conf /etc/nginx/sites-enabled/flask-front

sudo systemctl restart nginx

cat /etc/nginx/sites-enabled/flask-front
