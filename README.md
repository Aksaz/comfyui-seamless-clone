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
