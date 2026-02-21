"""
Image Generation Module

This module handles image generation/editing tasks using Stable Diffusion.
It processes images based on detection results and generates edited images.
"""
import argparse
import subprocess


def generate_image(img_path, prompt, lora_path, model_path, boxes_str, img_realname):
    """
    Generate or edit an image using Stable Diffusion based on detection boxes.
    
    Args:
        img_path (str): Path to the input image file
        prompt (str): Text prompt for image generation
        lora_path (str): Path to the LoRA model file
        model_path (str): Path to the Stable Diffusion model
        boxes_str (str): JSON string of detection boxes
        img_realname (str): Name of the image file
    
    Returns:
        None: Generated image is saved to output directory
    """
    env_name = "torchdraw"

    # Build conda run command
    cmd = ["conda", "run", 
        "-n", env_name, 
        "python", 
        "/home/GroundingDINO/demo/out/generation.py",
        img_path,
        prompt,
        lora_path,
        model_path,
        boxes_str,
        img_realname
        ] 
    print(cmd)
    try:
        # Execute command and capture output
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Generation task Command Output:", result)
    except subprocess.CalledProcessError as e:
        print(f"Error executing generation script: {e.returncode}, Error output: {e.stderr}")
    print("Generation task completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate or edit an image using Stable Diffusion.")
    parser.add_argument("img_path", help="Path to the image file.", default="/data/Imagebase/test.png")
    parser.add_argument("prompt", help="Text prompt for generation.", default="object")
    parser.add_argument("lora_path", help="Path to LoRA model file.", default="/data/lorafile/last_dyj.safetensors")
    parser.add_argument("model_path", help="Path to Stable Diffusion model.", default="/data/modelfile/gligen-1-4-inpainting-text-box")
    parser.add_argument("boxes_str", help="JSON string of detection boxes.", default=" ")
    parser.add_argument("img_realname", help="Name of the image file.", default="test.png")
    
    args = parser.parse_args()
    generate_image(args.img_path, args.prompt, args.lora_path, args.model_path, args.boxes_str, args.img_realname)

# Example usage:
# python detection.py '/data/Imagebase/test.png' 'house . person . dog' 'test.png'
# python generation.py '/data/Imagebase/art_dog_birthdaycake_W0sdgMf.png' 'tree' '/data/lorafile/jianbihua_v1.0.safetensors' '/data/modelfile/gligen-1-4-inpainting-text-box' '[[0.18, 0.30, 0.44, 0.52]]' 'art_dog_birthdaycake_W0sdgMf.png'

