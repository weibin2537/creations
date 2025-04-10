
import torch
import os
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import string
import argparse
from model import CaptchaCNN, CaptchaResNet

CHARS = string.ascii_lowercase + string.digits
CHAR2IDX = {c: i for i, c in enumerate(CHARS)}
IDX2CHAR = {i: c for c, i in CHAR2IDX.items()}

class CaptchaDataset(Dataset):
    def __init__(self, folder):
        self.images = []
        self.labels = []
        for name in os.listdir(folder):
            label = name.split("_")[0]
            self.images.append(os.path.join(folder, name))
            self.labels.append(label)
        self.transforms = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((60, 160)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = Image.open(self.images[idx])
        img = self.transforms(img)
        label = self.labels[idx]
        return img, torch.tensor([CHAR2IDX[c] for c in label])

def get_model(name, chars=4, classes=36):
    if name == "cnn":
        return CaptchaCNN(chars, classes)
    elif name == "resnet":
        return CaptchaResNet(chars, classes)
    else:
        raise ValueError("Unsupported backbone")

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backbone", choices=["cnn", "resnet"], default="cnn")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--data", type=str, default="dataset/train")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = get_model(args.backbone).to(device)
    loader = DataLoader(CaptchaDataset(args.data), batch_size=64, shuffle=True, num_workers=2, pin_memory=True)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(args.epochs):
        model.train()
        total_loss = 0
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            out = model(x).view(-1, len(CHARS))
            y = y.view(-1)
            loss = criterion(out, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), f"captcha_model_{args.backbone}.pth")
    print(f"✅ 模型保存为 captcha_model_{args.backbone}.pth")

if __name__ == "__main__":
    train()
