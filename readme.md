#### 机加系统服务层

- 主要功能：使用PG数据库为前端提供服务，与ERP进行数据交互
- 主要技术: python + flask

##### 目录结构

- MesService
  - lib 一些常用的封装，例如，操作PG数据库的方法。
  - modules 分模块进行业务代码管理
  - logs 日志文件
  - test 测试文件，单元测试等 
  - app.py 程序的入口
  - config.py 配置文件

##### 使用

- 依赖安装

 ```shell
pip install -r requestments.txt
 ```

- 项目启动

```shell
python app.py
```

