# CampusLink
Team-25
## CampusLink：校园失物招领平台
**GitHub仓库地址**：[https://github.com/Bistu-OSSDT-2026/CampusLink](https://github.com/Bistu-OSSDT-2026/CampusLink)
**项目属性**：开源软件开发课程小组实训项目 | 适配北京信息科技大学校园场景

## 项目概述
CampusLink是面向本校师生打造的轻量化Flask网页应用，用来解决线下纸质寻物启事传播范围窄、信息难同步、拾物人与失主对接不便的痛点。使用者可线上发布遗失、捡拾物品信息，完成图文上传、内容检索、个人发布条目管理，部署门槛低，适配校内日常使用需求。

## 技术构成
- 后端：Python 3.9+、Flask、Flask-SQLAlchemy、Flask-Login
- 本地数据库：SQLite（无需单独安装数据库服务）
- 前端技术：原生HTML、CSS（页面内嵌北京信息科技大学校徽元素）
- 版本协作工具：Git + GitHub

## 平台可用功能清单
1. 账号权限体系：支持注册、登录、登出；做访问拦截，未登录账号不能发布招领内容
2. 信息发布模块：区分「物品遗失」「捡到物品」两类条目，补充地点、文字描述，支持实拍图片上传
3. 首页内容陈列：按发布时间倒序展示全部公开的招领、寻物帖子
4. 模糊检索：依托标题、物品描述关键词筛选匹配相关帖子
5. 个人中心：集中查看本人发布记录，自主删除过期、作废内容，可标记物品已找回
6. 详情页：查阅完整物品资料、发布人联络方式，方便线下交接物品

## 本地部署启动步骤
### 1. 拉取线上仓库代码
```bash
git clone https://github.com/Bistu-OSSDT-2026/CampusLink.git
cd CampusLink
## 本地运行部署教程
### 1. Python环境要求
推荐Python 3.8 ~ 3.11版本，过低或过高会出现依赖兼容问题。

### 2. 安装项目依赖
打开终端，进入项目根目录执行：
pip install -r requirements.txt

### 3. 两种启动方式
#### Windows系统
cmd输入：
set FLASK_APP=主程序文件名.py
flask run

#### Mac/Linux系统
export FLASK_APP=主程序文件名.py
flask run

### 4. 访问项目
启动成功后浏览器打开 http://127.0.0.1:5000 即可进入页面

### 5. 停止运行
键盘按下 Ctrl + C 终止程序