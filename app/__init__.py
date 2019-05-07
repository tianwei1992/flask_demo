from flask import Flask

from configfile import Config    # 从同级的config.py文件导入...


app = Flask(__name__)
app.config.from_object(Config)  # 从configfile.py文件的Config类导入配置，解耦.其中app.config是Flask类的一个特性而不是configfile.py的文件名

from app import routes
