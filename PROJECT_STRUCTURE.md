# 项目结构说明

本文档详细说明项目的目录结构和各文件的作用。

## 根目录

```
servercopy/
├── .gitignore              # Git 忽略文件配置
├── README.md               # 项目主文档
├── SETUP.md                # 详细设置指南
├── CONTRIBUTING.md         # 贡献指南
├── PROJECT_STRUCTURE.md    # 本文件：项目结构说明
├── requirements.txt       # Python 依赖列表
├── env.example            # 环境变量配置示例
├── AIdrawG/               # Django Web 应用
├── GroundingDINO/         # GroundingDINO 目标检测模型
├── image_processing/      # 图像处理脚本
├── nginx/                 # Nginx 配置文件
└── scripts/               # 工具脚本（可选）
```

## AIdrawG/ - Django Web 应用

Django 项目的主要应用，提供 Web API 接口。

```
AIdrawG/
├── manage.py              # Django 管理脚本
├── start.sh               # 启动脚本
├── stop.sh                # 停止脚本
├── db.sqlite3             # SQLite 数据库（开发环境，不应提交）
├── aidrawapp/             # 主应用模块
│   ├── __init__.py
│   ├── models.py          # 数据模型（AidrawDB）
│   ├── views.py           # 视图函数（API 端点）
│   ├── admin.py           # Django 管理后台配置
│   ├── apps.py            # 应用配置
│   ├── tests.py           # 单元测试
│   └── function/          # 工具函数模块
│       ├── __init__.py
│       └── validators.py  # 验证函数（图片、提示词等）
├── AIdrawG/               # Django 项目配置
│   ├── __init__.py
│   ├── settings.py        # 项目设置（数据库、静态文件等）
│   ├── urls.py            # URL 路由配置
│   ├── wsgi.py            # WSGI 配置（生产环境）
│   └── asgi.py            # ASGI 配置（异步支持）
├── static/                # 静态文件
│   ├── html/              # JavaScript 和 CSS 文件
│   └── img/                # 图片资源
└── templates/             # HTML 模板
    └── home.html          # 主页模板
```

### 关键文件说明

- **views.py**: 包含两个主要 API 端点
  - `jsonvim()`: 处理检测和生成任务
  - `index()`, `home()`, `test()`: 页面视图

- **models.py**: 定义 `AidrawDB` 模型，存储：
  - 图片索引和路径
  - 提示词
  - 检测框数据（JSON）

- **validators.py**: 提供验证函数
  - `is_valid_image()`: 验证图片格式
  - `is_valid_prompttext()`: 验证提示词
  - `is_file_exists()`: 检查模型文件是否存在
  - `get_boxes()`: 读取检测框 JSON 文件

## GroundingDINO/ - 目标检测模型

基于 GroundingDINO 的目标检测实现。

```
GroundingDINO/
├── README.md              # GroundingDINO 官方文档
├── LICENSE                # 许可证
├── requirements.txt       # Python 依赖
├── setup.py              # 安装脚本
├── environment.yaml       # Conda 环境配置
├── Dockerfile            # Docker 配置
├── groundingdino/        # 核心模型代码
│   ├── config/           # 模型配置文件
│   ├── models/           # 模型定义
│   ├── util/             # 工具函数
│   └── datasets/         # 数据集处理
├── demo/                 # 演示和推理脚本
│   ├── inference_on_a_image.py  # 单图推理脚本
│   ├── gradio_app.py     # Gradio Web UI
│   └── diffusers/        # Diffusers 库（用于图像生成）
├── weights/              # 模型权重目录（需单独下载）
│   └── groundingdino_swint_ogc.pth
├── bert-base-uncased/    # BERT 模型文件（需下载）
└── logs/                 # 日志和输出目录
```

### 关键文件说明

- **demo/inference_on_a_image.py**: 执行目标检测的主脚本
- **groundingdino/config/**: 包含模型配置文件
  - `GroundingDINO_SwinT_OGC.py`: Swin-T 模型配置
  - `GroundingDINO_SwinB_cfg.py`: Swin-B 模型配置

## image_processing/ - 图像处理脚本

调用 GroundingDINO 和 Stable Diffusion 进行图像处理的脚本。

```
image_processing/
├── detection.py          # 目标检测脚本
└── generation.py         # 图像生成脚本
```

### 关键文件说明

- **detection.py**: 
  - 调用 GroundingDINO 进行目标检测
  - 使用 Conda 环境运行
  - 输出检测结果到 JSON 文件
  - 函数：`detect_objects(image_path, prompt, image_name)`

- **generation.py**:
  - 调用图像生成脚本
  - 传递检测框、提示词、LoRA 模型等参数
  - 使用 Stable Diffusion 进行图像编辑
  - 函数：`generate_image(img_path, prompt, lora_path, model_path, boxes_str, img_realname)`

## nginx/ - Web 服务器配置

Nginx 反向代理配置。

```
nginx/
└── conf.d/
    └── default.conf      # Nginx 服务器配置
```

### 配置说明

- 反向代理到 Django 应用（端口 8080）
- 静态文件服务
- 数据文件访问控制
- 文件上传大小限制

## scripts/ - 工具脚本

包含项目开发过程中使用的工具脚本（如文件名处理脚本等）。这些文件是可选的，通常不需要提交到 Git。

## 数据目录结构（服务器端）

项目运行时需要以下目录结构：

```
/data/
├── Imagebase/            # 上传的图片存储目录
├── lorafile/             # LoRA 模型文件目录
├── modelfile/            # Stable Diffusion 模型目录
├── boxesjson/            # 检测框 JSON 文件目录
└── detect_output/        # 检测输出目录
```

## 环境变量配置

项目使用环境变量进行配置，主要变量包括：

- **Django 设置**:
  - `DJANGO_SECRET_KEY`: Django 密钥
  - `DEBUG`: 调试模式
  - `ALLOWED_HOSTS`: 允许的主机

- **数据库配置**:
  - `DB_ENGINE`: 数据库引擎
  - `DB_NAME`: 数据库名称
  - `DB_HOST`: 数据库主机
  - `DB_PORT`: 数据库端口
  - `DB_USER`: 数据库用户
  - `DB_PASSWORD`: 数据库密码

- **路径配置**:
  - `STATIC_ROOT`: 静态文件根目录
  - `MEDIA_ROOT`: 媒体文件根目录
  - `IMAGE_BASE_PATH`: 图片基础路径
  - `LORA_MODELS_PATH`: LoRA 模型路径
  - `MODEL_DIR_PATH`: 模型目录路径

## 工作流程

1. **用户上传图片** → 存储到 `/data/Imagebase/`
2. **调用检测 API** → `image_processing/detection.py` → GroundingDINO 检测
3. **保存检测结果** → JSON 文件存储到 `/data/boxesjson/`
4. **数据库记录** → 保存到 `AidrawDB` 表
5. **调用生成 API** → `image_processing/generation.py` → Stable Diffusion 生成
6. **返回结果** → 生成后的图片路径

## 注意事项

1. **大文件**: 模型权重文件（`.pth`）和 BERT 模型文件较大，需要单独下载
2. **路径配置**: 项目中有多处硬编码路径，部署时需要根据实际情况修改
3. **Conda 环境**: 项目依赖特定的 Conda 环境 `torchdraw`
4. **权限**: 确保数据目录有正确的读写权限
5. **敏感信息**: 密码、密钥等敏感信息应使用环境变量管理，不要提交到 Git

