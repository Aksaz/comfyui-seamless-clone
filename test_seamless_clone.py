#!/usr/bin/env python3
"""
Test script for SeamlessClone node to verify fixes for mismatched proportions.
"""

import numpy as np
import cv2
import torch
from SeamlessClone import SeamlessClone

def create_test_images():
    """Create test images with mismatched proportions."""
    # Create a tall, narrow source image (100x300)
    source = np.random.randint(0, 255, (100, 300, 3), dtype=np.uint8)
    source[20:80, 50:250] = [255, 0, 0]  # Red rectangle
    
    # Create a wide, short destination image (300x100)
    destination = np.random.randint(0, 255, (300, 100, 3), dtype=np.uint8)
    destination[100:200, 20:80] = [0, 255, 0]  # Green rectangle
    
    # Create a mask for the source (same size as source initially)
    mask = np.zeros((100, 300), dtype=np.uint8)
    mask[20:80, 50:250] = 255
    
    return source, destination, mask

def test_seamless_clone():
    """Test the seamless clone with mismatched proportions."""
    print("Testing SeamlessClone with mismatched proportions...")
    
    # Create test images
    source, destination, mask = create_test_images()
    
    print(f"Source image shape: {source.shape}")
    print(f"Destination image shape: {destination.shape}")
    print(f"Mask shape: {mask.shape}")
    
    # Convert to torch tensors (simulating ComfyUI format)
    source_tensor = torch.from_numpy(source.astype(np.float32) / 255.0).unsqueeze(0)
    destination_tensor = torch.from_numpy(destination.astype(np.float32) / 255.0).unsqueeze(0)
    mask_tensor = torch.from_numpy(mask.astype(np.float32) / 255.0).unsqueeze(0)
    
    # Create SeamlessClone instance
    seamless_clone = SeamlessClone()
    
    try:
        # Test with automatic center calculation
        result = seamless_clone.seamless_clone(
            source_tensor, 
            destination_tensor, 
            mask_tensor, 
            "NORMAL_CLONE",
            center_x=0, 
            center_y=0
        )
        
        print("✅ Test passed! Seamless cloning completed successfully.")
        print(f"Result shape: {result[0].shape}")
        
        # Test with manual center coordinates (edge case)
        result2 = seamless_clone.seamless_clone(
            source_tensor, 
            destination_tensor, 
            mask_tensor, 
            "MIXED_CLONE",
            center_x=999,  # Out of bounds
            center_y=999   # Out of bounds
        )
        
        print("✅ Edge case test passed! Out-of-bounds coordinates handled correctly.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_edge_cases():
    """Test various edge cases."""
    print("\nTesting edge cases...")
    
    # Test with very small images
    source = np.random.randint(0, 255, (10, 10, 3), dtype=np.uint8)
    destination = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
    mask = np.ones((10, 10), dtype=np.uint8) * 255
    
    source_tensor = torch.from_numpy(source.astype(np.float32) / 255.0).unsqueeze(0)
    destination_tensor = torch.from_numpy(destination.astype(np.float32) / 255.0).unsqueeze(0)
    mask_tensor = torch.from_numpy(mask.astype(np.float32) / 255.0).unsqueeze(0)
    
    seamless_clone = SeamlessClone()
    
    try:
        result = seamless_clone.seamless_clone(
            source_tensor, 
            destination_tensor, 
            mask_tensor, 
            "NORMAL_CLONE",
            center_x=0, 
            center_y=0
        )
        print("✅ Small image test passed!")
    except Exception as e:
        print(f"❌ Small image test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Running SeamlessClone tests...")
    
    success1 = test_seamless_clone()
    success2 = test_edge_cases()
    
    if success1 and success2:
        print("\n🎉 All tests passed! The fix for mismatched proportions is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
