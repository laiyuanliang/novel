创建一个新目录，将这个项目代码拷贝至这个新建目录

#创建虚拟环境，本项目需要python3
virtualenv --no-site-packages --python=python3.6 venv

#激活虚拟环境
. venv/bin/activate

#安装项目所需的模块
pip install -r requirements

登录数据库，创建一个utf-8编码的数据库

根据上一步创建的数据库，修改当前目录下的config.py文件，包括用户名、密码、数据库名称

#用下面3条命令初始化数据库
python manage.py db init

python manage.py db migrate

python manage.py db upgrade

#运行项目
./start.sh
