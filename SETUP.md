# 项目设置指南

本文档提供详细的设置步骤，帮助您快速配置和运行项目。

## 前置要求

- Python 3.8 或更高版本
- CUDA（如果使用 GPU）
- MySQL 或 SQLite
- Conda（推荐，用于管理 Python 环境）

## 步骤 1: 环境准备

### 1.1 创建 Conda 环境

```bash
conda create -n torchdraw python=3.8
conda activate torchdraw
```

### 1.2 安装 PyTorch

根据您的 CUDA 版本安装 PyTorch：

```bash
# CUDA 11.3
conda install pytorch torchvision torchaudio pytorch-cuda=11.3 -c pytorch -c nvidia

# CPU only
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

## 步骤 2: 安装项目依赖

### 2.1 安装 Django 应用依赖

```bash
cd AIdrawG
pip install -r ../requirements.txt
```

### 2.2 安装 GroundingDINO

```bash
cd GroundingDINO
pip install -r requirements.txt
pip install -e .
```

**注意**: 如果遇到编译错误，请确保：
- 已设置 `CUDA_HOME` 环境变量（如果使用 GPU）
- 已安装必要的编译工具（gcc, g++）

## 步骤 3: 下载模型权重

```bash
cd GroundingDINO/weights
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
```

## 步骤 4: 配置数据库

### 选项 A: 使用 SQLite（开发环境）

无需额外配置，Django 会自动创建 SQLite 数据库。

### 选项 B: 使用 MySQL（生产环境）

1. 创建数据库：

```sql
CREATE DATABASE Aidrawsql CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 创建用户并授权：

```sql
CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON Aidrawsql.* TO 'your_username'@'localhost';
FLUSH PRIVILEGES;
```

3. 配置环境变量（见步骤 5）

## 步骤 5: 配置环境变量

复制 `env.example` 为 `.env` 并修改配置：

```bash
cp env.example .env
```

编辑 `.env` 文件，设置以下变量：

```bash
# Django 密钥（必须修改！）
DJANGO_SECRET_KEY=your-generated-secret-key

# 数据库配置
DB_ENGINE=django.db.backends.mysql
DB_NAME=Aidrawsql
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password

# 路径配置（根据实际部署环境修改）
IMAGE_BASE_PATH=/data/Imagebase
LORA_MODELS_PATH=/data/lorafile
MODEL_DIR_PATH=/data/modelfile
```

**生成 Django Secret Key**:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## 步骤 6: 创建必要的目录

```bash
# 创建数据目录
sudo mkdir -p /data/Imagebase
sudo mkdir -p /data/lorafile
sudo mkdir -p /data/modelfile
sudo mkdir -p /data/boxesjson
sudo mkdir -p /data/detect_output

# 设置权限
sudo chown -R $USER:$USER /data
```

## 步骤 7: 初始化数据库

```bash
cd AIdrawG
python manage.py makemigrations
python manage.py migrate
```

## 步骤 8: 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

## 步骤 9: 配置路径

根据您的实际部署环境，修改以下文件中的路径：

1. **AIdrawG/aidrawapp/views.py**
   - 修改图片存储路径（`/data/Imagebase`）
   - 修改 GroundingDINO 脚本路径

2. **image_processing/detection.py**
   - 修改 GroundingDINO 配置和权重路径
   - 修改输出路径

3. **image_processing/generation.py**
   - 修改生成脚本路径
   - 修改 Conda 环境名称

4. **AIdrawG/aidrawapp/function/validators.py**
   - 修改 LoRA 和模型文件路径

## 步骤 10: 运行开发服务器

```bash
cd AIdrawG
python manage.py runserver 0.0.0.0:8080
```

或使用提供的脚本：

```bash
cd AIdrawG
bash start.sh
```

## 步骤 11: 配置 Nginx（生产环境）

1. 复制 Nginx 配置：

```bash
sudo cp nginx/conf.d/default.conf /etc/nginx/conf.d/imageedit.conf
```

2. 编辑配置文件，修改：
   - `server_name`: 您的域名或 IP
   - `proxy_pass`: Django 服务地址
   - `alias`: 静态文件和数据目录路径

3. 测试配置：

```bash
sudo nginx -t
```

4. 重启 Nginx：

```bash
sudo systemctl restart nginx
```

## 故障排除

### 问题 1: `NameError: name '_C' is not defined`

**解决方案**: 重新安装 GroundingDINO：

```bash
cd GroundingDINO
pip uninstall groundingdino
pip install -e .
```

### 问题 2: CUDA 相关错误

**解决方案**: 检查 CUDA 环境：

```bash
echo $CUDA_HOME
nvidia-smi
```

如果 `CUDA_HOME` 未设置：

```bash
export CUDA_HOME=/usr/local/cuda  # 根据实际路径修改
```

### 问题 3: 数据库连接错误

**解决方案**:
- 检查 MySQL 服务是否运行：`sudo systemctl status mysql`
- 验证数据库用户权限
- 检查防火墙设置

### 问题 4: 权限错误

**解决方案**: 确保数据目录有正确的权限：

```bash
sudo chown -R $USER:$USER /data
chmod -R 755 /data
```

## 下一步

- 查看 [README.md](README.md) 了解 API 使用方法
- 查看各子目录的文档了解详细配置
- 在生产环境中使用 Gunicorn 和 Supervisor 管理进程

