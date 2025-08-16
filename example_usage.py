#!/usr/bin/env python3
"""
Example usage of the fixed SeamlessClone node.
This demonstrates how the node now handles mismatched proportions correctly.
"""

import numpy as np
import cv2
import torch
from SeamlessClone import SeamlessClone

def create_example_images():
    """Create example images that would cause the original issue."""
    # Create a tall source image (200x100)
    source = np.zeros((200, 100, 3), dtype=np.uint8)
    source[50:150, 25:75] = [255, 100, 100]  # Light red rectangle
    
    # Create a wide destination image (100x200)
    destination = np.zeros((100, 200, 3), dtype=np.uint8)
    destination[25:75, 50:150] = [100, 255, 100]  # Light green rectangle
    
    # Create a mask for the source
    mask = np.zeros((200, 100), dtype=np.uint8)
    mask[50:150, 25:75] = 255
    
    return source, destination, mask

def demonstrate_fix():
    """Demonstrate the fix for mismatched proportions."""
    print("Demonstrating SeamlessClone fix for mismatched proportions...")
    
    # Create example images
    source, destination, mask = create_example_images()
    
    print(f"Original source shape: {source.shape}")
    print(f"Original destination shape: {destination.shape}")
    print(f"Original mask shape: {mask.shape}")
    
    # Convert to torch tensors
    source_tensor = torch.from_numpy(source.astype(np.float32) / 255.0).unsqueeze(0)
    destination_tensor = torch.from_numpy(destination.astype(np.float32) / 255.0).unsqueeze(0)
    mask_tensor = torch.from_numpy(mask.astype(np.float32) / 255.0).unsqueeze(0)
    
    # Create SeamlessClone instance
    seamless_clone = SeamlessClone()
    
    print("\nTesting with automatic center calculation...")
    try:
        result = seamless_clone.seamless_clone(
            source_tensor, 
            destination_tensor, 
            mask_tensor, 
            "NORMAL_CLONE",
            center_x=0, 
            center_y=0
        )
        
        print("✅ Success! The fix works correctly.")
        print(f"Result shape: {result[0].shape}")
        
        # Convert result back to numpy for visualization
        result_np = (result[0][0].numpy() * 255).astype(np.uint8)
        
        # Save the result
        cv2.imwrite("example_result.jpg", cv2.cvtColor(result_np, cv2.COLOR_RGB2BGR))
        print("Result saved as 'example_result.jpg'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\nTesting with out-of-bounds center coordinates...")
    try:
        result2 = seamless_clone.seamless_clone(
            source_tensor, 
            destination_tensor, 
            mask_tensor, 
            "MIXED_CLONE",
            center_x=1000,  # Way out of bounds
            center_y=1000   # Way out of bounds
        )
        
        print("✅ Success! Out-of-bounds coordinates handled correctly.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("SeamlessClone Fix Demonstration")
    print("=" * 40)
    
    success = demonstrate_fix()
    
    if success:
        print("\n🎉 All demonstrations passed!")
        print("The fix successfully handles mismatched proportions and boundary issues.")
    else:
        print("\n❌ Some demonstrations failed.")
