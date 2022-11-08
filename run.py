import torch
import numpy as np
import torchvision
from PIL import Image
# a = Image.fromarray((torch.ones((3,1000,1000))*255).int().numpy())
x = torch.ones((100,100,3)).numpy()
x = (x * 255).astype(np.uint8)
a = Image.fromarray(x)
torchvision.transforms.ToPILImage()
print(a)
transforms2 = []
exec("""transforms2.append(torch.nn.Sequential(
    transforms.CenterCrop(10),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))))
""",{},{"transforms2":transforms2,"transforms":torchvision.transforms,"torch":torch})
print(transforms2[0](a))

# def func():
#     a = []
    
#     exec("global a; a.append((torch.zeros(100)))",{'a':a},{'torch':torch})  
#     print(a)
# a = 4
# func()
# print(a)

# def myfunc1():
# 	print('myfunc1')

# def myfunc2():
# 	print('myfunc2')

# globlsparam = {'__builtins__' : None}
# localsparam = {'myfunc1': myfunc1}

# exec('myfunc1()', globlsparam, localsparam) # valid
# exec('myfunc2', globlsparam, localsparam) # throws error