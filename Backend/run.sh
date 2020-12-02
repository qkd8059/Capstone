source "/home/ubuntu/.virtualenvs/backend/bin/activate"
export MY_IP=$(curl http://checkip.amazonaws.com)
export FLASK_APP="/home/ubuntu/Capstone/Backend/main.py"
export FLASK_ENV=development
flask run -p 5000
