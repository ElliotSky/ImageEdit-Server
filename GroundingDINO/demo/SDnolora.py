# ————SD没有lora版————

# 不显示警告
import warnings
warnings.filterwarnings("ignore")
# 基础包
import os
import torch
import numpy as np
from PIL import Image
import argparse
# SD包
from diffusers import StableDiffusionGLIGENPipeline
from diffusers.utils import load_image
# Grounding包
from torchvision.ops import box_convert
from groundingdino.models import build_model
from groundingdino.util.slconfig import SLConfig
from groundingdino.util.utils import clean_state_dict
from groundingdino.util.inference import annotate, load_image, predict
import groundingdino.datasets.transforms as T

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

def main(local_image_path, TEXT_PROMPT, prompt, phrases, outputurl):
    # load grounding dino
    def load_grounding_dino(device='gpu'):
        cache_config_file = '/home/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py' # 配置文件

        args = SLConfig.fromfile(cache_config_file) 
        model = build_model(args)
        args.device = device

        cache_file = '/home/GroundingDINO/weights/groundingdino_swint_ogc.pth' # 模型参数
        
        checkpoint = torch.load(cache_file, map_location='cpu')
        log = model.load_state_dict(clean_state_dict(checkpoint['model']), strict=False)
        print("Model loaded from {} \n => {}".format(cache_file, log))
        _ = model.eval()
        return model

    model = load_grounding_dino()

    # Load image
    # ! image_path !
    # local_image_path = '/home/AIdrawG/static/gener_work/art_dog_birthdaycake.png'

    image_source, image = load_image(local_image_path)
    Image.fromarray(image_source)
    # ! prompt !
    # TEXT_PROMPT = "dog"

    # import supervision as sv

    BOX_TRESHOLD = 0.55
    TEXT_TRESHOLD = 0.25

    boxes, logits, phrases = predict(
        model=model, 
        image=image, 
        caption=TEXT_PROMPT, 
        box_threshold=BOX_TRESHOLD, 
        text_threshold=TEXT_TRESHOLD
    )

    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    annotated_frame = annotated_frame[...,::-1] # BGR to RGB

    # image_source: np.ndarray
    # annotated_frame: np.ndarray

    def generate_masks_with_grounding(image_source, boxes):
        h, w, _ = image_source.shape
        boxes_unnorm = boxes * torch.Tensor([w, h, w, h])
        boxes_xyxy = box_convert(boxes=boxes_unnorm, in_fmt="cxcywh", out_fmt="xyxy").numpy()
        mask = np.zeros_like(image_source)
        for box in boxes_xyxy:
            x0, y0, x1, y1 = box
            mask[int(y0):int(y1), int(x0):int(x1), :] = 255
        return mask

    image_mask = generate_masks_with_grounding(image_source, boxes)
    Image.fromarray(annotated_frame)

    # Image Inpainting
    # 传参：prompt image_source boxes(tensor)
    image_source = Image.fromarray(image_source)
    annotated_frame = Image.fromarray(annotated_frame)
    image_mask = Image.fromarray(image_mask)

    image_source_for_inpaint = image_source.resize((512, 512))
    image_mask_for_inpaint = image_mask.resize((512, 512))

    num_box = len(boxes)

    xyxy_boxes = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").tolist()
    xyxy_boxes
    # if xyxy_boxes=[] return "没有找到prompt"

    # prompt = "monkey"
    # phrases = ["monkey"]

    # load stable diffusion
    pipe = StableDiffusionGLIGENPipeline.from_pretrained(
        "/data/modelfile/gligen-1-4-inpainting-text-box",
    )
    pipe = pipe.to("cuda")

    images = pipe(
        prompt=prompt,
        gligen_phrases=phrases,
        gligen_inpaint_image=image_source_for_inpaint,
        gligen_boxes=xyxy_boxes,
        gligen_scheduled_sampling_beta=1,
        output_type="pil",
        num_inference_steps=35,
    ).images

    images[0].save(outputurl)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an image and a prompt.")
    parser.add_argument("local_image_path", help="Path to the image file.",default="/data/Imagebase/test.png")
    parser.add_argument("TEXT_PROMPT", help="TEXT_PROMPT.",default="house")
    parser.add_argument("phrases", help="phrases.",default="rose rose rose rose")
    parser.add_argument("prompt", help="Path to the prompt text file.",default=["rose","rose","rose","rose"])
    parser.add_argument("outputurl", help="outputurl.",default="/data/geren_output/test.png")

    args = parser.parse_args()

    # 调用主函数，传入解析到的参数
    main(args.local_image_path, args.TEXT_PROMPT, args.prompt, args.phrases, args.outputurl)

    # python SDnolora.py /data/Imagebase/test.png "house" "rose rose rose rose" ["rose" "rose" "rose" "rose"] /data/geren_output/test.png