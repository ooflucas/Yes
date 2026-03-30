import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
torch.backends.cudnn.benchmark = True
# ============================================
# 1. CONVOLUTIONAL AUTOENCODER (Sharper!)
# ============================================
class ConvAutoencoder(nn.Module):
    def __init__(self, latent_dim=20):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 32, 3, stride=2, padding=1), # 28 -> 14
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), # 14 -> 7
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, 7, stride=1, padding=0), # 7 -> 1
            nn.ReLU()
        )
        self.fc_mu = nn.Linear(128, latent_dim)
        self.fc_logvar = nn.Linear(128, latent_dim)
        self.fc_decode = nn.Linear(latent_dim, 128)
        
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 7, stride=1, padding=0),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 1, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        x = x.view(-1, 1, 28, 28)
        h = self.encoder(x).view(-1, 128)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        z = self.reparameterize(mu, logvar)
        z_reshaped = self.fc_decode(z).view(-1, 128, 1, 1)
        return self.decoder(z_reshaped).view(-1, 784), mu, logvar
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
def train(model, device, epochs=5000, batch_size=128): # 3060Ti 轻松跑 128
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    # 使用新版 AMP 缩放器
    scaler = torch.amp.GradScaler('cuda') 
    
    model.train()
    print(f"🚀 Training on {torch.cuda.get_device_name(0)} (8GB VRAM)")

    for epoch in range(epochs):
        inputs, targets = create_batch(batch_size) # 假设你之前的 create_batch 函数还在
        inputs, targets = inputs.to(device), targets.to(device)

        optimizer.zero_grad(set_to_none=True)

        # 正确的新版 Autocast 语法
        with torch.amp.autocast('cuda'):
            output, mu, logvar = model(inputs)
            loss = vae_loss_fn(output, targets, mu, logvar, beta=0.5)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        if epoch % 500 == 0:
            print(f"Epoch {epoch:5d} | Loss: {loss.item():.4f}")
    
    print("-" * 50)
    print("Training complete!")
    
    # Plot loss curve
    plt.figure(figsize=(10, 5))
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss Over Time (Convolutional Autoencoder)')
    plt.grid(True)
    plt.show()
    
    return


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
    train(model_conv, device, epochs=1000, batch_size=8, noise_level=1.0)
    
    # Visualize results
    print("\n" + "="*50)
    print("VISUALIZING RESULTS")
    print("="*50)
    generate_samples(model_conv, device)
