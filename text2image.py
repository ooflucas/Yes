import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# ============================================
# 1. CONVOLUTIONAL AUTOENCODER (Sharper!)
# ============================================
class ConvAutoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=7, stride=1, padding=0),
            nn.ReLU()
        )
        self.fc_mu = nn.Linear(128, 20)
        self.fc_logvar = nn.Linear(128, 20)
        self.fc_decode = nn.Linear(20, 128)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=7, stride=1, padding=0),
            nn.ReLU(),
            # Layer 2: 7x7 → 14x14 (32 channels)
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            
            # Layer 3: 14x14 → 28x28 (1 channel)
            nn.ConvTranspose2d(32, 1, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )
    def reparameterize(self, mu, logvar):
        # 從 logvar (對數方差) 算出標準差 std
        # 數學上：std = sqrt(exp(logvar)) = exp(0.5 * logvar)
        std = torch.exp(0.5 * logvar)
        
        # 產生一個跟 std 形狀一樣的隨機噪音 (從標準常態分佈 N(0,1) 抽樣)
        eps = torch.randn_like(std)
        
        # z = mu + std * eps
        return mu + eps * std
    def forward(self, x):
        # Input: (batch, 784) → reshape to (batch, 1, 28, 28)
        x = x.view(-1, 1, 28, 28)
        h = self.encoder(x)
        h = h.view(-1, 128)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        z = self.reparameterize(mu, logvar)
        z_expanded = self.fc_decode(z)
        z_reshaped = z_expanded.view(-1, 128, 1, 1)
        # Decode
        decoded = self.decoder(z_reshaped)  # Shape: (batch, 1, 28, 28)
        
        # Flatten back to (batch, 784)
        return decoded.view(-1, 784), mu, logvar

# ============================================
# 2. CREATE TRAINING DATA (SQUARES WITH NOISE)
# ============================================
def create_batch(batch_size=64, noise_level=1.0):
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
        noise = torch.randn(28, 28) * noise_level
        noisy = torch.clamp(square + noise, 0.0, 1.0)
        
        inputs.append(noisy.view(-1))
        targets.append(square.view(-1))
    
    return torch.stack(inputs), torch.stack(targets)


# ============================================
# 3. LOSS FUNCTION
# ============================================
def vae_loss_fn(recon_x, x, mu, logvar, beta):
    # 使用 functional 版本的 BCE 比較不會有縮進問題
    BCE = nn.functional.binary_cross_entropy(recon_x, x, reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return BCE + beta * KLD


# ============================================
# 4. TRAINING FUNCTION
# ============================================
def train(model, device, epochs=3000, batch_size=64, noise_level=1.0):
    optimizer = optim.Adam(model.parameters(), lr=0.0005)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, 
        mode='min',
        patience=500,
        factor=0.5
    )
    loss_history = []
    
    print(f"Training on: {device}")
    print(f"Model: Convolutional Autoencoder")
    print(f"Epochs: {epochs}, Batch size: {batch_size}")
    print(f"Noise level: {noise_level}")
    print("-" * 50)
    
    for epoch in range(epochs):
        # Create batch
        inputs, targets = create_batch(batch_size, noise_level)
        
        # Move to GPU/CPU
        inputs = inputs.to(device)
        targets = targets.to(device)
        
        # Forward pass
        output, mu, logvar = model(inputs)
        loss = vae_loss_fn(output, targets, mu, logvar, beta=0.5)
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step(loss)
        
        loss_history.append(loss.item())
        
        # Print progress
        if epoch % 500 == 0:
            current_lr = optimizer.param_groups[0]['lr']
            print(f"Epoch {epoch:4d}, LR: {current_lr:.6f}, Loss: {loss.item():.6f}")
    
    print("-" * 50)
    print("Training complete!")
    print(f"Final loss: {loss_history[-1]:.6f}")
    
    # Plot loss curve
    plt.figure(figsize=(10, 5))
    plt.plot(loss_history)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Time (Convolutional Autoencoder)')
    plt.grid(True)
    plt.show()
    
    return loss_history


# ============================================
# 5. VISUALIZATION FUNCTION
# ============================================
def visualize(model, device, num=6, noise_level=1):
    model.eval()
    
    with torch.no_grad():
        # Create test batch
        inputs, targets = create_batch(num, noise_level)
        inputs = inputs.to(device)
        targets = targets.to(device)
        
        # Reconstruct
        outputs, mu, logvar = model(inputs)
        
        # Move to CPU for display
        inputs = inputs.cpu()
        targets = targets.cpu()
        outputs = outputs.cpu()
        
        # Create figure
        fig, axes = plt.subplots(num, 3, figsize=(12, 3 * num))
        
        for i in range(num):
            # Noisy input
            axes[i, 0].imshow(inputs[i].view(28, 28), cmap='gray')
            axes[i, 0].set_title(f'Noisy Input (noise={noise_level})', fontsize=10)
            axes[i, 0].axis('off')
            
            # Clean target
            axes[i, 1].imshow(targets[i].view(28, 28), cmap='gray')
            axes[i, 1].set_title('Clean Target', fontsize=10)
            axes[i, 1].axis('off')
            
            # Reconstructed
            axes[i, 2].imshow(outputs[i].view(28, 28), cmap='gray')
            axes[i, 2].set_title('Reconstructed (Sharper!)', fontsize=10)
            axes[i, 2].axis('off')
        
        plt.suptitle('Convolutional Autoencoder - Much Sharper Results!', fontsize=14)
        plt.tight_layout()
        plt.show()
def generate_samples(model, device, num=6):
    model.eval()
    with torch.no_grad():
        # 從「標準常態分佈」隨機抓取 20 維的向量
        z = torch.randn(num, 20).to(device)
        
        # 只跑 Decoder 的後半段
        z_expanded = model.fc_decode(z)
        z_reshaped = z_expanded.view(-1, 128, 1, 1)
        samples = model.decoder(z_reshaped).cpu()
        
        fig, axes = plt.subplots(1, num, figsize=(15, 3))
        for i in range(num):
            axes[i].imshow(samples[i].view(28, 28), cmap='gray')
            axes[i].axis('off')
        plt.suptitle("VAE Generated Squares from Random Noise")
        plt.show()
if __name__ == "__main__":
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Create convolutional model
    model_conv = ConvAutoencoder().to(device)
    print(f"Conv Model parameters: {sum(p.numel() for p in model_conv.parameters()):,}")
    
    # Train convolutional model
    print("\n" + "="*50)
    print("TRAINING CONVOLUTIONAL AUTOENCODER")
    print("="*50)
    train(model_conv, device, epochs=100000, batch_size=64, noise_level=1.0)
    
    # Visualize results
    print("\n" + "="*50)
    print("VISUALIZING RESULTS")
    print("="*50)
    generate_samples(model_conv, device)
