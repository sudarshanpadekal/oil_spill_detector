from torchvision import datasets, transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

datasets = datasets.ImageFolder("dataset/", transform=transform)
