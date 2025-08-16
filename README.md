# ComfyUI Seamless Clone Node

[![Publish to Comfy registry](https://github.com/Aksaz/comfyui-seamless-clone/actions/workflows/publish_action.yml/badge.svg)](https://github.com/Aksaz/comfyui-seamless-clone/actions/workflows/publish_action.yml)

![Seamless Clone Example](https://amroamroamro.github.io/mexopencv/opencv/cloning_demo_01.png)

A custom node for ComfyUI that implements OpenCV's seamless cloning functionality, allowing you to blend images naturally using Poisson blending techniques.

## Features

-   Seamless image blending using OpenCV's

-   Three blending modes:

    -   NORMAL_CLONE: Standard seamless

    -   MIXED_CLONE: Mixed seamless cloning that preserves gradients

    -   MONOCHROME_TRANSFER: Monochrome transfer mode

-   Automatic or manual center point selection
-   Compatible with ComfyUI's image processing pipeline
-   **Robust handling of mismatched image proportions** - automatically resizes and validates boundaries
-   **Fallback blending** - if seamless cloning fails, falls back to simple alpha blending

## Installation

1. Navigate to your ComfyUI custom nodes directory:

```sh
cd ComfyUI/custom_nodes/
```

2. Clone this repository:

```sh
git clone https://github.com/Aksaz/comfyui-seamless-clone
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage

The node accepts the following inputs:

-   source_image: The image to be cloned (foreground)
-   destination_image: The target image (background)
-   mask_image: A binary mask defining the region to be cloned
-   blend_mode: Choose between NORMAL_CLONE, MIXED_CLONE, or MONOCHROME_TRANSFER

-   center_x: X-coordinate of the clone center (optional)
-   center_y: Y-coordinate of the clone center (optional)

Output:

-   `cloned_image`: The resulting seamlessly blended image

### Important Notes

-   **Image Proportions**: The node automatically resizes the source image and mask to match the destination image dimensions to prevent boundary errors.
-   **Center Point Validation**: If center coordinates are provided, they are automatically clamped to valid image boundaries.
-   **Fallback Mode**: If seamless cloning fails due to complex geometry or boundary issues, the node automatically falls back to simple alpha blending.
-   **Mask Validation**: The mask is automatically cropped to ensure it fits within the destination image bounds.

## Troubleshooting

### Common Issues

1. **"Mask is empty after processing"**: Ensure your mask contains non-zero values in the region you want to clone.

2. **"No valid mask pixels found"**: Check that your mask image has visible content in the areas you want to clone.

3. **Seamless cloning falls back to alpha blending**: This is normal behavior when the geometry is too complex for seamless cloning. The result will still be a blended image, though without the advanced Poisson blending.

### Best Practices

-   Use masks with clear, well-defined boundaries for best results
-   Ensure the source image has good contrast with the destination image
-   For complex shapes, consider using the MIXED_CLONE mode which preserves gradients better

## Requirements

-   numpy==2.2.0
-   opencv_python==4.10.0.84
-   torch==2.5.1

## Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the existing style and includes appropriate documentation updates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

This node utilizes OpenCV's seamless cloning implementation based on the paper "Seamless Image Cloning and Editing" by Patrick Pérez, Michel Gangnet, and Andrew Blake.
