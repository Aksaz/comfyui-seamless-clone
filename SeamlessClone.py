import torch
import cv2
import numpy as np

class SeamlessClone:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_image": ("IMAGE",),
                "destination_image": ("IMAGE",),
                "mask_image": ("MASK",),
                "blend_mode": (["NORMAL_CLONE", "MIXED_CLONE", "MONOCHROME_TRANSFER"],),
                "center_x": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "center_y": ("INT", {"default": 0, "min": 0, "max": 8192}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("cloned_image",)
    CATEGORY = "Image Processing"
    FUNCTION = "seamless_clone"

    def seamless_clone(self, source_image, destination_image, mask_image, blend_mode, center_x=None, center_y=None):

        # Ensure batch size is 1 for simplicity
        if source_image.shape[0] != 1 or destination_image.shape[0] != 1 or mask_image.shape[0] != 1:
            raise ValueError("Batch size greater than 1 is not supported.")

        # Convert images to numpy arrays and scale to [0, 255]
        source_image_np = (source_image[0].cpu().numpy() * 255).astype(np.uint8)
        destination_image_np = (destination_image[0].cpu().numpy() * 255).astype(np.uint8)

        # Mask is in [0,1] range (since it's a torch.Tensor)
        mask_np = mask_image[0].cpu().numpy()

        # Get destination image dimensions
        dest_h, dest_w = destination_image_np.shape[:2]
        
        # Get source image dimensions
        source_h, source_w = source_image_np.shape[:2]
        
        # Resize source image and mask to match destination image size
        source_image_np = cv2.resize(
            source_image_np, (dest_w, dest_h), interpolation=cv2.INTER_LINEAR
        )
        mask_np = cv2.resize(
            mask_np, (dest_w, dest_h), interpolation=cv2.INTER_LINEAR
        )

        # Ensure mask is single-channel
        if mask_np.ndim == 3 and mask_np.shape[2] > 1:
            mask_np = cv2.cvtColor(mask_np, cv2.COLOR_RGB2GRAY)
        elif mask_np.ndim == 3:
            mask_np = mask_np[:, :, 0]

        # Ensure mask is binary (0 or 255)
        mask_np = (mask_np > 0.5).astype(np.uint8) * 255

        # Check if mask is empty
        if np.count_nonzero(mask_np) == 0:
            # Mask is empty; cannot proceed
            raise ValueError("Mask is empty after processing.")

        # Convert images to BGR for OpenCV
        source_image_cv = cv2.cvtColor(source_image_np, cv2.COLOR_RGB2BGR)
        destination_image_cv = cv2.cvtColor(destination_image_np, cv2.COLOR_RGB2BGR)

        # Calculate the center of the mask if center_x and center_y are not provided
        if center_x == 0 and center_y == 0:
            # Use the geometric center of the mask bounding box
            mask_indices = np.argwhere(mask_np > 0)
            if len(mask_indices) == 0:
                raise ValueError("No valid mask pixels found.")
            
            # Calculate bounding box center instead of center of mass
            min_y, min_x = mask_indices.min(axis=0)
            max_y, max_x = mask_indices.max(axis=0)
            center_x = (min_x + max_x) // 2
            center_y = (min_y + max_y) // 2
            
            print(f"Mask bounds: min_y={min_y}, max_y={max_y}, min_x={min_x}, max_x={max_x}")
            print(f"Geometric center: ({center_x}, {center_y})")
        else:
            # When custom center is provided, we need to ensure the source image is positioned correctly
            # The source image is already resized to match destination, so we use the provided center directly
            print(f"Using custom center: ({center_x}, {center_y})")
            
            # When using custom center, we might need to adjust the source image to align with the mask
            # Get the mask bounds to understand where the actual content should be
            mask_indices = np.argwhere(mask_np > 0)
            if len(mask_indices) > 0:
                min_y, min_x = mask_indices.min(axis=0)
                max_y, max_x = mask_indices.max(axis=0)
                mask_center_x = (min_x + max_x) // 2
                mask_center_y = (min_y + max_y) // 2
                
                # Calculate offset needed to align source with the custom center
                offset_x = center_x - mask_center_x
                offset_y = center_y - mask_center_y
                
                print(f"Mask center: ({mask_center_x}, {mask_center_y})")
                print(f"Offset needed: ({offset_x}, {offset_y})")
                
                # Apply offset to the source image
                if offset_x != 0 or offset_y != 0:
                    # Create a translation matrix
                    M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
                    source_image_cv = cv2.warpAffine(source_image_cv, M, (dest_w, dest_h))
                    print(f"Applied translation to source image")

        # Validate and clamp center coordinates to image boundaries
        center_x = max(0, min(center_x, dest_w - 1))
        center_y = max(0, min(center_y, dest_h - 1))
        
        # Use the calculated or provided center coordinates
        clone_center = (center_x, center_y)

        print(f"clone_center: {clone_center}")
        print(f"destination image size: {dest_w}x{dest_h}")
        
        # Ensure mask is within image bounds by clipping coordinates
        # This preserves the exact mask shape while ensuring it fits within the image
        mask_indices = np.argwhere(mask_np > 0)
        if len(mask_indices) > 0:
            # Check if any mask pixels are outside image bounds
            valid_mask = (mask_indices[:, 0] >= 0) & (mask_indices[:, 0] < dest_h) & \
                        (mask_indices[:, 1] >= 0) & (mask_indices[:, 1] < dest_w)
            
            if not np.all(valid_mask):
                # Remove invalid mask pixels that are outside image bounds
                valid_indices = mask_indices[valid_mask]
                mask_np = np.zeros_like(mask_np)
                if len(valid_indices) > 0:
                    mask_np[valid_indices[:, 0], valid_indices[:, 1]] = 255
                    # Recalculate center based on valid mask pixels
                    valid_center = valid_indices.mean(axis=0).astype(int)
                    clone_center = (valid_center[1], valid_center[0])
                    print(f"adjusted clone_center: {clone_center}")
                else:
                    raise ValueError("No valid mask pixels found within image bounds.")
        
        # Map blend_mode string to OpenCV constant
        blend_mode_dict = {
            "NORMAL_CLONE": cv2.NORMAL_CLONE,
            "MIXED_CLONE": cv2.MIXED_CLONE,
            "MONOCHROME_TRANSFER": cv2.MONOCHROME_TRANSFER,
        }
        mode = blend_mode_dict.get(blend_mode, cv2.NORMAL_CLONE)

        try:
            # Perform seamless cloning
            output_cv = cv2.seamlessClone(
                source_image_cv, destination_image_cv, mask_np, clone_center, mode
            )
        except cv2.error as e:
            # If seamless cloning fails, fall back to simple blending
            print(f"Seamless cloning failed: {e}")
            print("Falling back to simple alpha blending...")
            
            # Create a simple alpha blend as fallback
            mask_normalized = mask_np.astype(np.float32) / 255.0
            if mask_normalized.ndim == 2:
                mask_normalized = np.stack([mask_normalized] * 3, axis=-1)
            
            # Blend images using the mask
            output_cv = (source_image_cv * mask_normalized + 
                        destination_image_cv * (1 - mask_normalized)).astype(np.uint8)

        # Convert output to RGB
        output_rgb = cv2.cvtColor(output_cv, cv2.COLOR_BGR2RGB)

        # Convert to torch.Tensor and scale to [0, 1]
        output_tensor = torch.from_numpy(output_rgb.astype(np.float32) / 255.0)

        # Add batch dimension
        output_tensor = output_tensor.unsqueeze(0)  # Shape [1, H, W, C]

        return (output_tensor,)