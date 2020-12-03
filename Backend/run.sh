source "/home/hp/anaconda3/bin/activate"
conda activate EddieServer
# export MY_IP=$(curl http://checkip.amazonaws.com)
export MY_IP='home.tech'
export FLASK_APP="/home/hp/servers/EddieCapstone/Backend/main.py"
export FLASK_ENV=development
flask run -p 5000
