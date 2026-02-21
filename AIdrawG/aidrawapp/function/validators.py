# validators.py
import os
import json
import imghdr

# 文件合法校验
def is_valid_image(file):
    """
    检查上传的文件是否为有效的图片。
    
    参数:
    - file: Django的UploadedFile对象
    
    返回:
    - 如果是有效图片则返回True，否则返回False
    """
    # 检查文件是否为图片
    image_type = imghdr.what(file)
    if not image_type:
        return False
    print(image_type)
    # 这里可以添加对图片格式的进一步检查，例如：
    allowed_formats = ['jpeg','jpg', 'png']
    return image_type.lower() in allowed_formats

# 提示语合法校验
def is_valid_prompttext(prompttext):
    """
    检查提示语是否合法。
    
    参数:
    - prompttext: 用户输入的字符串
    
    返回:
    - 如果输入合法则返回True，否则返回False
    """
    # 示例检查：非空且长度不超过100字符
    return bool(prompttext) and len(prompttext) <= 100

# lora与model存在校验
LORA_MODELS_PATH = '/data/lorafile'
MODEL_DIR_PATH = '/data/modelfile'
def is_file_exists(lora_name, model_name):
    """
    检查指定路径下是否存在指定的文件。
    """
    lora_path = os.path.join(LORA_MODELS_PATH, lora_name)
    model_path = os.path.join(MODEL_DIR_PATH, model_name)
    
    lora_exists = os.path.exists(lora_path)
    model_exists = os.path.exists(model_path)
    
    if not lora_exists:
        return {"error": f"Lora model '{lora_name}' does not exist on the server."}, False
    if not model_exists:
        return {"error": f"Model '{model_name}' does not exist on the server."}, False
    
    return (lora_path,model_path), True

def split_and_validate(prompt,num):
    # 按空格拆分字符串
    words = prompt.split()
    # 校验数量，这里以4个词作为预期数量，可以根据实际情况调整
    if len(words) == num:
        return True
    else:
        return False

def get_boxes(image_index):
    only_image_name, file_ext = os.path.splitext(image_index) # 无后缀文件名
    pred_json_path = '/data/boxesjson/' + only_image_name + ".json"
    
    try:
        with open(pred_json_path, 'r') as json_file:
            data = json.load(json_file)
            
            if 'boxes_array' in data:
                return data['boxes_array']
            else:
                print("Error: 'boxes_array' key not found in the JSON file.")
                return None
    except FileNotFoundError:
        print(f"Error: The file {pred_json_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON file {pred_json_path}.")
        return None

# def box2xyxyboxes(boxes):
        # # 转换为PyTorch张量并归一化边界框坐标
    # boxes_tensor = torch.tensor(boxes, dtype=torch.float32)
    # width, height = image_source.size
    # normalized_boxes_tensor = boxes_tensor.clone()
    # normalized_boxes_tensor[:, 0::2] /= width
    # normalized_boxes_tensor[:, 1::2] /= height
    # xyxy_boxes = normalized_boxes_tensor.tolist()

