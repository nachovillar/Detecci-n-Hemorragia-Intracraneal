# Import the required libraries
import torch
import torchvision
from torchvision.io import read_image
from torchvision.utils import draw_bounding_boxes

# read input image from your computer
img = read_image('../train_data_fusion/CQ500-CT-0-2-9.png')

# bounding box are xmin, ymin, xmax, ymax
box = [0.504805986328125, 0.395365146484375, 0.08005615234375, 0.08988765625]
box = torch.tensor(box)
print(box)
box = box.unsqueeze(0)
print(box)

# draw bounding box and fill color
img = draw_bounding_boxes(img, box, width=5, colors=(255,255,255), fill=True)

# transform this image to PIL image
img = torchvision.transforms.ToPILImage()(img)

# display output
img.show()
