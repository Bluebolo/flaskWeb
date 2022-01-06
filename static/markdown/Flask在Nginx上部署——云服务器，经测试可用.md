将Flask部署Nginx上

> 注意：
按照参考文章配置在我的服务器上运行有问题。如果按照文章进行出现错误，请尝试文末的**我的配置**

## 安装

### 安装Python3,pip

```
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```

### 安装python3虚拟环境

安装虚拟环境还是很有必要的，例如刚开始我没有装，直接用系统的python3，到uwsgi启动时，遇到很多问题。Ubuntu 16.04 上有预装了2.7，3.5两个python版本。
   
```
sudo pip install virtualenv           #安装virtualenv
mkdir flask_uwsgi                     #创建部署flask的文件夹
cd flask_uwsgi
virtualenv -p /usr/bin/python3 env    #创建虚拟环境 
source env/bin/activate            #激活虚拟环境
deactivate                            #退出虚拟环境
```

### 安装Flask

安装Flask，使网站能够运行。

```
(env) ubuntu@0705:~/flask_uwsgi$ pip install flask
```

之后编辑myapp.py

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/moco")
def moco():
    return "Hello moco!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
	
```

运行  `python myapp.py`,出现如下，即成功，可以curl 127.0.0.0.1:5000访问。


### 安装uwsgi（官方中文文档）

uwsgi使一个web服务器，flask是一个web框架。他们之间通过wsgi协议进行通讯。详情看uwsgi、wsgi和nginx的区别和关系。

`(env) ubuntu@0705:~/flask_uwsgi$pip install uwsgi`

如果报下如下错误，先装依赖，如果再执行完成之后，还是失败，重新建立虚拟环境。　

```
sudo apt-get install aptitude
sudo apt-get install  build-essential python-dev
sudo apt-get install python3-dev
```


安装uwsgi成功后，创建一个文件测试下。

```
test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    #return ["Hello World"] # python2
    return [b"Hello World"] # python3
``` 

然后，运行uWSGI：
　　`uwsgi --http :8000 --wsgi-file uwsgi_test.py`
  
参数含义：

- http :8000：使用http协议，8000端口
- wsgi-file uwsgi_test.py:加载指定文件uwsgi_test.py


## uwsgi部署Flask 

这里简化下，就用uwsgi部署1中的myapp.py。新建一个config.ini文件，内容如下。

```
[uwsgi]
http=127.0.0.1:5000
#虚拟环境中的目录，这里env后边不要/bin
home = /home/ubuntu/flask_uwsgi/env
#启动的文件
wsgi-file =  /home/ubuntu/flask_uwsgi/myapp.py
# python 程序内用以启动的 application 变量名,不加callable=app，访问时报服务器错误Internal Server Errorcallable=app
# 处理器数
processes = 1
# 线程数
threads = 1
buffer-size = 32768
master = true
stats=/home/ubuntu/flask_uwsgi/uwsgi.status
pidfile=/home/ubuntu/flask_uwsgi/uwsgi.pid

```

执行 uwsgi config.ini ，项目启动成功后，curl 127.0.0.1:5000/moco , curl 127.0.0.1:5000 进行验证。

## nginx通过uwsgi部署Flask 
修改config.ini 配置，socket一项有变化,
启动uwsgi， uwsgi config.ini

```
[uwsgi]
socket = 127.0.0.1:5000
home = /home/ubuntu/flask_uwsgi/env
wsgi-file =  /home/ubuntu/flask_uwsgi/myapp.py
callable=app
processes = 1
threads = 1
buffer-size = 32768
master = true
stats=/home/ubuntu/flask_uwsgi/uwsgi.status
pidfile=/home/ubuntu/flask_uwsgi/uwsgi.pid
```

 修改nginx配置，

 重新加载nginx，sudo nginx -s reload
 
```
server {
	listen 80;
    server_name a.ozflhnb.top;
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:5000;
     }
}
```


<font color='red'>以下是我的配置：</font>

## 我的配置

> 此处config部分按照参考文章2设置

uwsgi:

```

[uwsgi] 
# 必须全部为绝对路径 
# 项目的路径 ，pwd指令中显示的路径
chdir = /usr/share/personal/flask_web
# flask的wsgi文件 
wsgi-file = /usr/share/personal/flask_web/app.py
# 回调的app对象 
callable = app 
# Python虚拟环境的路径 ， 进入到虚拟环境目录里面执行pipenv --venv得到 
home = /usr/share/personal/flask_web/env
# 进程相关的设置 
# 主进程 
master = true 
# 最大数量的工作进程 
processes = 10
# 项目中使用的端口 
#http = :5000
socket = 127.0.0.1:5000
# 设置socket的权限 最大权限是777
chmod-socket = 666 
# 退出的时候是否清理环境 
vacuum = true


```

nginx:

```

server {
        # 监听的端口号 
        listen 80;
        # 域名
        server_name ; # 此处是域名，记得填上
        charset utf-8;
        # 最大的文件上传尺寸
        client_max_body_size 75M;
        location / {
			include uwsgi_params;
			uwsgi_pass 127.0.0.1:5000;
     	}
}

```

---

参考文章：

[通过Nginx部署flask项目](https://www.cnblogs.com/sdadx/p/10360208.html)

[Flask项目实战——13—(项目部署到阿里云服务器和本地服务器)](https://blog.csdn.net/weixin_42118531/article/details/106592752)