"""
Object Detection Module

This module handles object detection tasks using GroundingDINO.
It processes images and detects objects based on text prompts.
"""
import argparse
import subprocess


def detect_objects(image_path, prompt, image_name):
    """
    Perform object detection on an image using GroundingDINO.
    
    Args:
        image_path (str): Path to the input image file
        prompt (str): Text prompt describing objects to detect
        image_name (str): Name of the image file
    
    Returns:
        None: Detection results are saved to output directory
    """
    outdata_path = '/data/detect_output' 
    env_name = "torchdraw"

    # Build conda run command
    cmd = ["conda", "run", 
        "-n", env_name, 
        "python", 
        "/home/GroundingDINO/demo/inference_on_a_image.py",
        "-c", "/home/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py",
        "-p", "/home/GroundingDINO/weights/groundingdino_swint_ogc.pth",
        "-i", image_path,
        "-o", outdata_path,
        "-t", prompt,
        "-n", image_name
        ] 

    try:
        # Execute command and capture output
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Detection task Command Output:", result)
    except subprocess.CalledProcessError as e:
        print(f"Error executing detection script: {e}")
    print("Detection task completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect objects in an image using GroundingDINO.")
    parser.add_argument("image_path", help="Path to the image file.")
    parser.add_argument("prompt", help="Text prompt describing objects to detect.")
    parser.add_argument("image_name", help="Name of the image file.")
    
    args = parser.parse_args()
    detect_objects(args.image_path, args.prompt, args.image_name)

