"""
Image Processing Module

This module provides image processing functionality including:
- Object detection using GroundingDINO
- Image generation/editing using Stable Diffusion
"""

from .detection import detect_objects
from .generation import generate_image

__all__ = ['detect_objects', 'generate_image']

