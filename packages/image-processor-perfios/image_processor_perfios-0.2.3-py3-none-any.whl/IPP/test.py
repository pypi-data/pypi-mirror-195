import onnxruntime
import numpy as np
from PIL import Image
from Image_Preprocessor import image_mnist
# Load the ONNX model
model_path = "mnist.onnx"
session = onnxruntime.InferenceSession(model_path)
image = Image.open("img_59.jpg")
tensor = image_mnist(image)
np_array = tensor.cpu().detach().numpy()
# Define a sample input
input_name = session.get_inputs()[0].name
input_data = np_array

# Run inference on the input
output_name = session.get_outputs()[0].name
output = session.run([output_name], {input_name: input_data})[0]
prediction = np.argmax(output[0],axis=0)
print(prediction)