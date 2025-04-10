
import torch.nn as nn
import torchvision.models as models

class CaptchaCNN(nn.Module):
    def __init__(self, num_chars=4, num_classes=36):
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

class CaptchaResNet(nn.Module):
    def __init__(self, num_chars=4, num_classes=36):
        super(CaptchaResNet, self).__init__()
        resnet = models.resnet18(pretrained=False)
        resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        resnet.fc = nn.Identity()
        self.backbone = resnet
        self.fc = nn.Linear(512, num_chars * num_classes)

    def forward(self, x):
        x = self.backbone(x)
        return self.fc(x)
