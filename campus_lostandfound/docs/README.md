# 校园失物招领平台

一款基于 Python + Tkinter 的桌面失物招领应用，使用本地 JSON 文件存储数据。

## 项目结构

```
campus_lostandfound/
├── src/                    # 源代码目录
│   ├── main.py             # 应用入口
│   ├── models/             # 数据模型层
│   │   ├── __init__.py
│   │   └── item.py         # 失物数据模型
│   ├── services/           # 业务服务层
│   │   ├── __init__.py
│   │   └── data_service.py # JSON数据CRUD服务
│   ├── ui/                 # 用户界面层
│   │   ├── __init__.py
│   │   ├── main_window.py  # 主窗口
│   │   ├── post_dialog.py  # 发布对话框
│   │   └── search_dialog.py # 搜索对话框
│   └── utils/              # 工具配置层
│       ├── __init__.py
│       └── config.py       # 配置常量
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── test_item_model.py  # 数据模型测试
│   └── test_data_service.py # 数据服务测试
├── docs/                   # 文档目录
│   ├── README.md
│   ├── requirements.md     # 需求规格说明
│   └── user_manual.md      # 用户手册
├── data/                   # 数据存储目录
│   └── lost_items.json     # JSON数据文件
├── presentation/           # 演示材料
│   └── PPT_OUTLINE.md      # 答辩PPT框架
├── requirements.txt        # 依赖说明
└── run.sh                  # 运行脚本
```

## 功能特性

- **失物发布**：发布遗失物品信息，包括名称、类型、描述、地点、联系人等
- **物品搜索**：支持按关键词、类型、状态、地点等多条件搜索
- **状态管理**：标记物品为"已找到"或"丢失中"
- **数据持久化**：使用本地 JSON 文件存储，无需数据库
- **详情查看**：双击查看物品详细信息

## 技术栈

- Python 3.8+
- Tkinter (Python标准库)
- dataclasses (数据模型)
- json (数据存储)
- pytest (测试框架)

## 快速开始

### 环境要求

- Python 3.8 或更高版本

### 安装依赖

```bash
pip install pytest
```

### 运行应用

```bash
cd campus_lostandfound
python src/main.py
```

或使用运行脚本：

```bash
chmod +x run.sh
./run.sh
```

### 运行测试

```bash
cd campus_lostandfound
python -m pytest tests/ -v
```

## 团队分工

| 角色 | 职责 | 提交内容 |
|------|------|----------|
| 架构师 | 整体架构设计、项目配置、模块接口定义 | `src/main.py`、`src/utils/config.py`、项目结构 |
| 开发1 | UI层开发 | `src/ui/main_window.py`、`src/ui/post_dialog.py`、`src/ui/search_dialog.py` |
| 开发2 | 数据层开发 | `src/models/item.py`、`src/services/data_service.py` |
| 产品文档 | 需求分析、文档编写 | `docs/requirements.md`、`docs/user_manual.md` |
| 测试 | 测试用例编写、测试执行 | `tests/test_item_model.py`、`tests/test_data_service.py`、测试报告 |

## 开发规范

1. 代码遵循 PEP 8 规范
2. 使用类型注解
3. 每个模块包含清晰的文档字符串
4. 测试覆盖核心功能
5. 提交前运行测试确保无错误

## 许可证

MIT License