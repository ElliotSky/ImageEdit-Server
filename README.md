# ImageEdit Server

基于 GroundingDINO 和 Stable Diffusion 的图像编辑服务器项目。该项目提供了一个 Web 接口，支持图像中的目标检测和基于检测结果的图像生成/编辑功能。

## 项目结构

```
servercopy/
├── AIdrawG/              # Django Web 应用
│   ├── aidrawapp/        # 主应用模块
│   │   ├── function/     # 工具函数（验证器等）
│   │   ├── models.py     # 数据模型
│   │   └── views.py      # 视图函数
│   ├── AIdrawG/          # Django 项目配置
│   │   ├── settings.py   # 项目设置
│   │   └── urls.py       # URL 路由
│   ├── static/           # 静态文件（CSS, JS, 图片）
│   ├── templates/        # HTML 模板
│   ├── manage.py         # Django 管理脚本
│   ├── start.sh          # 启动脚本
│   └── stop.sh           # 停止脚本
├── GroundingDINO/        # GroundingDINO 目标检测模型
│   ├── groundingdino/    # 核心模型代码
│   ├── demo/             # 演示和推理脚本
│   ├── weights/          # 模型权重（需单独下载）
│   └── requirements.txt  # Python 依赖
├── image_processing/     # 图像处理脚本
│   ├── detection.py      # 目标检测脚本
│   └── generation.py     # 图像生成脚本
├── nginx/                # Nginx 配置文件
│   └── conf.d/
│       └── default.conf  # Nginx 服务器配置
└── scripts/              # 工具脚本（可选）

```

## 功能特性

1. **目标检测（Detection）**
   - 基于 GroundingDINO 模型进行零样本目标检测
   - 支持自然语言描述的目标检测
   - 返回检测框坐标和置信度

2. **图像生成/编辑（Generation）**
   - 基于检测结果进行图像编辑
   - 支持 LoRA 模型和 Stable Diffusion 模型
   - 可指定编辑区域和提示词

## 环境要求

- Python 3.8+
- Django 4.2+
- PyTorch
- CUDA（推荐，用于 GPU 加速）
- MySQL 或 SQLite（数据库）
- Nginx（生产环境）

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd servercopy
```

### 2. 安装 Python 依赖

#### Django 应用依赖

```bash
cd AIdrawG
pip install django pymysql
```

#### GroundingDINO 依赖

```bash
cd GroundingDINO
pip install -r requirements.txt
pip install -e .
```

### 3. 下载模型权重

```bash
cd GroundingDINO/weights
# 下载 GroundingDINO 预训练模型
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
```

### 4. 配置数据库

编辑 `AIdrawG/AIdrawG/settings.py`，配置数据库连接信息：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 或 'sqlite3'
        'NAME': 'your_database_name',
        'HOST': 'localhost',
        'PORT': 3306,
        'USER': 'your_username',
        'PASSWORD': 'your_password',
    }
}
```

### 5. 初始化数据库

```bash
cd AIdrawG
python manage.py makemigrations
python manage.py migrate
```

### 6. 配置路径

根据你的服务器环境，修改以下文件中的路径：

- `AIdrawG/aidrawapp/views.py` - 图片存储路径
- `image_processing/detection.py` - 目标检测脚本路径
- `image_processing/generation.py` - 图像生成脚本路径
- `AIdrawG/aidrawapp/function/validators.py` - LoRA 和模型路径

## 使用方法

### 启动开发服务器

```bash
cd AIdrawG
python manage.py runserver 0.0.0.0:8080
```

或使用提供的脚本：

```bash
cd AIdrawG
bash start.sh
```

### API 接口

#### 1. 目标检测接口

**POST** `/jsonvim/`

请求参数：
- `tasktype`: `"detection"`
- `file`: 图片文件
- `userInput`: 检测提示词（如 "chair . person . dog"）

响应示例：
```json
{
    "imageindex": "/path/to/image.jpg"
}
```

#### 2. 图像生成接口

**POST** `/jsonvim/`

请求参数：
- `tasktype`: `"generation"`
- `imageindex`: 图片路径（来自检测接口）
- `prompt`: 生成提示词
- `loraname`: LoRA 模型文件名
- `modelname`: Stable Diffusion 模型名称
- `boxes`: 检测框 JSON（可选，默认使用检测结果）

响应示例：
```json
{
    "gerenImg_url": "generated_image.png"
}
```

## 生产环境部署

### Nginx 配置

参考 `nginx/conf.d/default.conf` 配置 Nginx 反向代理。

### 使用 Gunicorn（推荐）

```bash
pip install gunicorn
gunicorn AIdrawG.wsgi:application --bind 0.0.0.0:8080
```

## 注意事项

1. **模型权重文件**：由于文件较大，模型权重文件（`.pth`）需要单独下载，不在 Git 仓库中。

2. **路径配置**：项目中的硬编码路径需要根据实际部署环境进行调整。

3. **环境变量**：建议使用环境变量管理敏感信息（数据库密码、密钥等）。

4. **GPU 支持**：如需使用 GPU，确保已安装 CUDA 并正确配置 `CUDA_HOME` 环境变量。

5. **Conda 环境**：项目使用 Conda 环境 `torchdraw`，需要先创建并配置该环境。

## 依赖说明

### Django 应用
- Django 4.2+
- PyMySQL
- Pillow（图像处理）

### GroundingDINO
- PyTorch
- torchvision
- transformers
- opencv-python
- 其他依赖见 `GroundingDINO/requirements.txt`

## 文档

- [SETUP.md](SETUP.md) - 详细的安装和配置指南
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构详细说明
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南

## 参考资源

- [GroundingDINO 官方仓库](https://github.com/IDEA-Research/GroundingDINO)
- [Django 文档](https://docs.djangoproject.com/)
- [Stable Diffusion](https://github.com/Stability-AI/StableDiffusion)

## 贡献

欢迎提交 Issue 和 Pull Request！详情请查看 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

请查看各子项目的许可证文件：
- GroundingDINO: 见 `GroundingDINO/LICENSE`
- Django 应用: 根据项目需求设置

