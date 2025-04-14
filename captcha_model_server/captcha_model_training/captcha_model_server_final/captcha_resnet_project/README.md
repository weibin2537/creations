
# ResNet18 验证码识别训练包

## 使用方法

1. 安装依赖：

    pip install torch torchvision pillow

2. 使用 CNN 模型训练：

    python train.py --backbone cnn

3. 使用 ResNet18 模型训练：

    python train.py --backbone resnet

输出模型为：captcha_model_resnet.pth
