## USAGE
    sudo apt-get install git mysql python-django
    sudo mysqld_safe -uroot
    mysql -uroot
    create database zheye;
    git clone https://github.com/azurefang/zheye.git
    cd zheye
    sudo pip install -r requirements.txt
    ./manage.py syncdb
    ./manage.py runserver
