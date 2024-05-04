# Description: Enum class to define the user information. If you want to add a new model type or device info .. etc, you can add it here.
# =========================================================
from enum import Enum


class DeviceInfo(Enum):
    CPU = 0
    GPU = 1
    TPU = 2
    FPGA = 3
    VPU = 4
    OTHERS = 5


class ModelType(Enum):
    KERAS = 0
    TENSORFLOW_SAVEDMODEL = 1
    PYTORCH = 2
    ONNX = 3
    OTHERS = 4
    TORCHSCRIPT = 5
    OPENVINO = 6
    TENSOR_RT = 7
    COREML = 8
    TENSORFLOW_GRAPHDEF = 9
    TENSORFLOW_LITE = 10
    TENSORFLOW_EDGE_TPU = 11
    TENSORFLOW_JS = 12
    PADDLEPADDLE = 13
    MXNET = 14
    CAFFE = 15
    OTHERS = 16
