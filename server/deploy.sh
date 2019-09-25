cd ~
source ~/env/bin/activate
cd ggg/
git pull
pip install -r requirements.txt
./manage.py migrate
./manage.py collectstatic
sudo supervisorctl restart ggg
