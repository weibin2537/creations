import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import string

# 支持字符集：a-z + 0-9
CHARS = string.ascii_lowercase + string.digits
CHAR_SET_LEN = len(CHARS)
CAPTCHA_LENGTH = 4

# ✅ 将输出 tensor 解码成字符串
def decode_prediction(output_tensor):
    out = output_tensor.view(-1, CAPTCHA_LENGTH, CHAR_SET_LEN)
    out_max = out.argmax(2)
    return ''.join([CHARS[i] for i in out_max[0]])

# ✅ 图像预处理函数（用于推理）
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((60, 160)),
        transforms.ToTensor(),              # 转为 1x60x160
    ])
    return transform(image)

# ✅ CNN 模型结构（轻量）
class CaptchaCNN(nn.Module):
    def __init__(self, num_chars=CAPTCHA_LENGTH, num_classes=CHAR_SET_LEN):
        super(CaptchaCNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2, 2),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 7 * 20, 1024), nn.ReLU(),
            nn.Linear(1024, num_chars * num_classes)
        )

    def forward(self, x):
        return self.fc(self.conv(x))

# ✅ ResNet18 模型结构（推荐）
class CaptchaResNet(nn.Module):
    def __init__(self, num_chars=CAPTCHA_LENGTH, num_classes=CHAR_SET_LEN):
        super(CaptchaResNet, self).__init__()
        resnet = models.resnet18(pretrained=False)
        resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        resnet.fc = nn.Identity()
        self.backbone = resnet
        self.fc = nn.Linear(512, num_chars * num_classes)

    def forward(self, x):
        x = self.backbone(x)
        return self.fc(x)
