sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-dev
sudo apt install python3.10-distutils
sudo apt install python3.10-venv
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt