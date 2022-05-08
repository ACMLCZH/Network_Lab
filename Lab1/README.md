+ 文件结构：
    + `server.py`：运行服务器的主程序，负责接收探测数据、处理并储存进数据库
    + `info_extract.py`：负责解析探测数据并提取出有用字段
    + `loadJson2db.py`：负责将字段数据存储进MySQL中
    + `trace.py`：负责读取处理后的数据，绘制路径
    + `trianglation.py`：负责完成三角定位算法
    + `test_server.py`：可以使用 `sample_wifi_data.txt` 中的数据模拟嗅探器客户端进行测试
+ 运行方法：
    + `python server.py`：运行服务器，在本地IP及7788端口上开启
    + `python ./trace.py ./trace.csv`：将 `trace.csv` 中的路径数据可视化
