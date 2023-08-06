import torch
import onnx
from model import mnist

# Load the PyTorch model
model = mnist()

# Export the model to ONNX format
dummy_input = torch.randn(1, 784)
print(dummy_input)
output_file = "mnist.onnx"
torch.onnx.export(model, dummy_input, output_file, verbose=True)
