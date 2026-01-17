Manaswi Gaur
Final Test Accuracy: 99.07 (98.54% without fine tuning)
Data augmentation techniques used: 
- Resize(256)
- RandomCrop(224)
- RandomHorizontalFlip
- RandomRotation(15 degrees)
- ColorJitter (brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1)
- ToTensor
- Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
Learning rate schedule used - torch.optim.lr_scheduler.ReduceLROnPlateau
Bonus Challenges Attempted: 
- Bonus 1: Fine-tuning
- Bonus 3: Visualize Predictions