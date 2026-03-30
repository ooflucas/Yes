import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# ============================================
# 1. AUTOENCODER MODEL
# ============================================
class Autoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(784, 512), nn.ReLU(),
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 32)
        )
        self.decoder = nn.Sequential(
            nn.Linear(32, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
            nn.Linear(256, 512), nn.ReLU(),
            nn.Linear(512, 784),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))


# ============================================
# 2. CREATE TRAINING DATA (SQUARES WITH NOISE)
# ============================================
def create_batch(batch_size=64):
    inputs = []
    targets = []
    
    for _ in range(batch_size):
        # Clean square (random position and size)
        square = torch.zeros(28, 28)
        size = torch.randint(4, 15, (1,)).item()
        x = torch.randint(0, 28 - size, (1,)).item()
        y = torch.randint(0, 28 - size, (1,)).item()
        square[y:y+size, x:x+size] = 1.0
        
        # Add noise
        noise = torch.randn(28, 28) * 0.06
        noisy = torch.clamp(square + noise, 0.0, 1.0)
        
        inputs.append(noisy.view(-1))
        targets.append(square.view(-1))
    
    return torch.stack(inputs), torch.stack(targets)


# ============================================
# 3. LOSS FUNCTION
# ============================================
def loss_fn(output, target):
    bce = nn.BCELoss()(output, target)
    mse = nn.MSELoss()(output, target)
    return 0.3 * mse + 0.7 * bce


# ============================================
# 4. TRAINING FUNCTION
# ============================================
def train(model, device, epochs=3000, batch_size=64):
    optimizer = optim.Adam(model.parameters(), lr=0.0005)
    loss_history = []
    
    print(f"Training on: {device}")
    print(f"Epochs: {epochs}, Batch size: {batch_size}")
    print("-" * 40)
    
    for epoch in range(epochs):
        # Create batch
        inputs, targets = create_batch(batch_size)
        
        # Move to GPU/CPU
        inputs = inputs.to(device)
        targets = targets.to(device)
        
        # Forward pass
        output = model(inputs)
        loss = loss_fn(output, targets)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        loss_history.append(loss.item())
        
        # Print progress
        if epoch % 500 == 0:
            print(f"Epoch {epoch:4d}, Loss: {loss.item():.6f}")
    
    print("-" * 40)
    print("Training complete!")
    
    # Plot loss curve
    plt.figure(figsize=(10, 5))
    plt.plot(loss_history)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Time')
    plt.grid(True)
    plt.show()
    
    return loss_history


# ============================================
# 5. VISUALIZATION FUNCTION
# ============================================
def visualize(model, device, num=6):
    model.eval()
    
    with torch.no_grad():
        # Create test batch
        inputs, targets = create_batch(num)
        inputs = inputs.to(device)
        targets = targets.to(device)
        
        # Reconstruct
        outputs = model(inputs)
        
        # Move to CPU for display
        inputs = inputs.cpu()
        targets = targets.cpu()
        outputs = outputs.cpu()
        
        # Create figure
        fig, axes = plt.subplots(num, 3, figsize=(12, 3 * num))
        
        for i in range(num):
            # Noisy input
            axes[i, 0].imshow(inputs[i].view(28, 28), cmap='gray')
            axes[i, 0].set_title('Noisy Input', fontsize=10)
            axes[i, 0].axis('off')
            
            # Clean target
            axes[i, 1].imshow(targets[i].view(28, 28), cmap='gray')
            axes[i, 1].set_title('Clean Target', fontsize=10)
            axes[i, 1].axis('off')
            
            # Reconstructed
            axes[i, 2].imshow(outputs[i].view(28, 28), cmap='gray')
            axes[i, 2].set_title('Reconstructed', fontsize=10)
            axes[i, 2].axis('off')
        
        plt.tight_layout()
        plt.show()


# ============================================
# 6. MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Create model
    model = Autoencoder().to(device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Train
    train(model, device, epochs=3000, batch_size=64)
    
    # Visualize results
    visualize(model, device, num=6)
