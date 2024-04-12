 echo "BUILD START"
 python3.9 -m pip install Django==4.2.11
 python3.9 -m pip install -r requirements.txt
 python3.9 manage.py collectstatic --noinput --clear
 echo "BUILD END"
 