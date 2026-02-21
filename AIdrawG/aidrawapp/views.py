# 第二版 更新：1.整合了jsonvim函数 2.增加test通路
import os
import json
import subprocess
from .models import AidrawDB
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from aidrawapp.function.validators import is_valid_image, is_valid_prompttext, is_file_exists, get_boxes, split_and_validate


# Create your views here.

def index(request):
    print("open home.html")
    return render(request, "home.html")
    
def home(request):
    return HttpResponse("web 维护中 请晚上再试！")

@csrf_exempt
def test(request):
    if request.method == 'POST':
        return HttpResponse("web 维护中 请晚上再试！")
    else:
        # 如果不是POST请求，可以处理GET请求或直接渲染页面
        return render(request, "test1.html")

@csrf_exempt
def jsonvim(request):
    print("open json")
    if request.method == 'POST':
        task_type = request.POST.get('tasktype')
        
        if task_type == 'detection':
            # 执行目标检测任务
            uploadImage = request.FILES.get('file')
            prompttext = request.POST.get('userInput')

            # 使用验证函数检查文件和输入
            if not is_valid_image(uploadImage):
                return JsonResponse({"error": "Please check the pictures according to the documentation"}, status=400)

            if not is_valid_prompttext(prompttext):
                return JsonResponse({"error": "Please check the prompt according to the documentation"}, status=400)

            # 保存图片，返回唯一路径
            server_root = '/data/Imagebase'
            fs = FileSystemStorage(location='/data/Imagebase')
            img_path = fs.save(uploadImage.name, uploadImage)
            img_url = fs.url(img_path)
            img_realname = os.path.basename(img_path)
            img_absolute_path = '/data/Imagebase'+img_url

            print("get a detection task:")
            print("prompttext:",prompttext)
            print("imagename:",img_realname)
            print("serverurl:",img_absolute_path)

            
            # 执行目标检测任务
            cmd = ["python", "/home/GroundingDINO0/detection.py", img_absolute_path, prompttext, img_realname]
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                # print(result)
                boxes_json = get_boxes(img_realname)
                # 数据存入数据库
                detectdata = AidrawDB(
                    image_index=img_realname,
                    image_path=img_url,
                    prompt_text=prompttext,  # 使用用户输入作为prompt_text
                    boxes=boxes_json,
                )

                detectdata.save()
                print("save ok")
                return JsonResponse({"imageindex": img_url}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        
        elif task_type == 'generation':
            # Handling generation tasks
            image_path = request.POST.get('imageindex')
            prompt = request.POST.get('prompt')
            lora_name = request.POST.get('loraname')
            model_name = request.POST.get('modelname')
            boxes_str = request.POST.get('boxes')
            print("start check")
            # 空值检验
            if not image_path or not lora_name or not model_name:
                return JsonResponse({"error": "Missing required parameters for generation task"}, status=400)

            # lora,model 存在检验
            error_message, files_exist = is_file_exists(lora_name, model_name)
            if not files_exist:
                return JsonResponse(error_message, status=400)
            else:
                lora_path,model_path = error_message

            print("get a generation task:")
            print(image_path)
            print(prompt)
            print(lora_path)
            print(model_path)
            print(boxes_str)

            # 获取图片路径
            try:
                print("start sql")
                detectdata = AidrawDB.objects.get(image_path=image_path)
                img_path = '/data/Imagebase'+image_path
                img_realname = detectdata.image_index
                print(img_path,img_realname)
                if boxes_str == 'false': # 手动检测/自动检测
                    boxes_str = detectdata.boxes
                    if not split_and_validate(prompt,len(boxes_str)):
                        return JsonResponse({"error":"prompt_num not = boxes_num"}, status=404)
                    boxes_str = json.dumps(boxes_str)
                print(boxes_str)
            except AidrawDB.DoesNotExist:
                # 如果没有找到匹配的记录，则返回错误信息
                return JsonResponse({"error": f"No data found for imageindex: {img_realname}."}, status=404)
             
            #参数：img_path, prompt, lora_path, model_path, boxes_str, img_realname
            cmd = ["python", "/home/GroundingDINO0/generation.py", img_path, prompt, lora_path, model_path, boxes_str, img_realname]
            try:
                result = subprocess.run(cmd, check=True, capture_output=True, text=True)
                # print(result)
                return JsonResponse({"gerenImg_url": img_realname}, status=200)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        
        else:
            return JsonResponse({"error": "Unsupported task type"}, status=400)
    
    return HttpResponse("Welcome to the AI Task Manager. Use POST requests with 'tasktype' parameter.", status=200)