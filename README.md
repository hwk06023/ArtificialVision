# ArtificialVision

<img src="https://lh3.googleusercontent.com/u/0/drive-viewer/AEYmBYSOMvdeaLCLq2djzo1mgZIEd6-Qyll8boR6V7Z1VHYkH2IFJzg8geBFdcxis-KIyVdoawhJTa-mWCLmfImUXQIoCJVv8w=w1762-h1610" width=550> <br/>

[![PyPI version](https://badge.fury.io/py/artificialvision.svg)](https://badge.fury.io/py/artificialvision)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub pull requests](https://img.shields.io/github/issues-pr/hwk06023/ArtificialVision)
![GitHub contributors](https://img.shields.io/github/contributors/hwk06023/ArtificialVision)
![GitHub stars](https://img.shields.io/github/stars/hwk06023/ArtificialVision?style=social)

<br/>

**The package is still under development and has not been released yet.**  <br/>

**If next version is released, This message will be removed and this package will be available.**  <br/>

<br/>

## Installation


```bash
pip install artificialvision
```

<br/>

## What is ArtificialVision?

ArtificialVision is the package for makes it easy to get the outcomes of various Machine Learning & Computer Vision technologies.
This package's aims are improving the quality and increasing the productivity by using it for convenience in various research and development experiments. <br/>

In this Version, just inference & getting the various results are supported. Support for training and fine-tuning will be added in the future. <br/>

<br/>

## Contributing to ArtificialVision

All the contributions are welcome ! <br/>

Check the [ContributeGuide.md](ContributeGuide.md) for more information. <br/>




### Contributors

<img src = "https://contrib.rocks/image?repo=hwk06023/ArtificialVision"/>

<br/> <br/>






## Methods Tutorial

### Image Classification

**example**  <br/>

```python
from artificialvision import ImgClassification
import cv2 

# Read the image
img = cv2.imread('PATH of Image file')

# Get the classification result
ImgClassification.get_result(img)
```

### Object Detection

**example**  <br/>

```python
from artificialvision import ObjDetection
import cv2

''' Image '''
# Read the image
img = cv2.imread('PATH of Image file')

# Get the detection result with the bounding box
ObjDetection.get_result(img)

# Get the bounding box only
ObjDetection.get_result_with_box(img)

''' Video '''
# Read the video
video = cv2.VideoCapture('PATH of Video file', type=1)

# Get the detection result with the bounding box
ObjDetection.get_result(video)

# Get the bounding box only
ObjDetection.get_result_with_box(video)
```

**hyperparameters**  <br/>

- `type` : int, default is 0
    - 0 : Image
    - 1 : Video 

<br/> <br/>



### Segmentation

**example**  <br/>

```python
from artificialvision import Segmentation
import cv2

''' Image '''
# Read the image
img = cv2.imread('PATH of Image file')

# Get the segmentation result
Segmentation.get_result(img)

# Get only the segment map
Segmentation.get_segment_map(img)
''' Video '''
# Read the video
video = cv2.VideoCapture('PATH of Video file', type=1)

# Get the segmentation result
Segmentation.get_result(video)

# Get only the segment map
Segmentation.get_segment_map(video)
''' Webcam (real-time) '''
# start the webcam(recording)
# if finished, press 'q' to stop & get the result
Segmentation.get_result(type=2)
```

**hyperparameters**  <br/>

- `type` : int, default is 0
    - 0 : Image
    - 1 : Video 
    - 2 : Webcam (real-time)

- `category` : int, default is 0
    - segmentation category
    - 0 : Semantic Segmentation
    - 1 : Instance Segmentation
    - 2 : Panoptic Segmentation

- `detail` : int, default is 0
    - segmentation detail
    - 0 : Segmentation Result (Overlayed Image)
    - 1 : Segmentation Map

- `get_poligon` : bool, default is False
    - If True, get the poligon points of the segmentation result. (Only for the instance segmentation)

<br/> <br/>



### Image Matching

**example**  <br/>
 
```python
from artificialvision import ImgMatching
import cv2 

''' Image '''
# Read the images
img1 = cv2.imread('PATH of Image1 file')
img2 = cv2.imread('PATH of Image2 file')

# Get the matching score
ImgMatching.get_matching_score(img1, img2)

# Get the matching result
ImgMatching.get_matching_result(img1, img2)


''' Video '''
# Read the videos
video1 = cv2.VideoCapture('PATH of Video1 file')
video2 = cv2.VideoCapture('PATH of Video2 file')

# Get the matching score
ImgMatching.get_matching_score(video1, video2, type=1)

# Get the matching result
ImgMatching.get_matching_result(video1, video2, type=1)

''' Mixed '''
# Read the images for matchin
img_list = [img1, img2, img3, ...]

# Get the matching score
ImgMatching.get_matching_score(img_list, video1, type=2)

# Get the matching result
ImgMatching.get_matching_result(img_list, video1, type=2)

''' Webcam (real-time) '''
# start the webcam(recording)
# if finished, press 'q' to stop & get the result
ImgMatching.get_matching_result(img_list, type=3)
```

**hyperparameters**  <br/>

- `type` : int, default is 0
    - 0 : Image
    - 1 : Video 
    - 2 : Mixed
    - 3 : Webcam (real-time)
- `threshold` : float, default is 0.5
    - The threshold for the matching score. If the matching score is less than the threshold, it is considered as a matching result. Range is 0.0 ~ 1.0. Recommended is +-0.1 from the default value.
    

<br/> 

## Format

### Inference Data Format

| Inference data format                                                                           | Type in python                                        | Usage Example                  |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------ |
| [Path of the data](#Methods-Tutorial)                                                           | ```str```                                             | '/Path/to/data/file.extension' |
| [List](#Methods-Tutorial)                                                                       | ```list```                                            | 
| [Numpy Array](#Methods-Tutorial)                                                                | ```numpy.ndarray```                                   |
| [Pytorch Tensor](#Methods-Tutorial)                                                             | ```torch.Tensor```                                    |
| [Tensorflow Tensor](#Methods-Tutorial)                                                          | ```tensorflow.python.framework.ops.EagerTensor```     |

### Inference Model Format

| Inference model format                                                     | `export.py --include` | Model                     |
|:---------------------------------------------------------------------------|:----------------------|:--------------------------|
| [PyTorch](https://pytorch.org/)                                            | -                     | `model.pt`              |
| [TorchScript](https://pytorch.org/docs/stable/jit.html)                    | `torchscript`         | `model.torchscript`     |
| [ONNX](https://onnx.ai/)                                                   | `onnx`                | `model.onnx`            |
| [OpenVINO](https://docs.openvino.ai/latest/index.html)                     | `openvino`            | `model_openvino_model/` |
| [TensorRT](https://developer.nvidia.com/tensorrt)                          | `engine`              | `model.engine`          |
| [CoreML](https://github.com/apple/coremltools)                             | `coreml`              | `model.mlmodel`         |
| [TensorFlow SavedModel](https://www.tensorflow.org/guide/saved_model)      | `saved_model`         | `model_saved_model/`    |
| [TensorFlow GraphDef](https://www.tensorflow.org/api_docs/python/tf/Graph) | `pb`                  | `model.pb`              |
| [TensorFlow Lite](https://www.tensorflow.org/lite)                         | `tflite`              | `model.tflite`          |
| [TensorFlow Edge TPU](https://coral.ai/docs/edgetpu/models-intro/)         | `edgetpu`             | `model_edgetpu.tflite`  |
| [TensorFlow.js](https://www.tensorflow.org/js)                             | `tfjs`                | `model_web_model/`      |
| [PaddlePaddle](https://github.com/PaddlePaddle)                            | `paddle`              | `model_paddle_model/`   |


------

<br/>

**If you want to more information, check the [Official Docs(Not yet)]()**

<br/>



