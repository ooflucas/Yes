import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os

# ============================================
# 0. CONFIGURATION
# ============================================
CONFIG = {
    "latent_dim": 64, 
    "num_classes": 2, 
    "epochs": 1000,           # More epochs since we have more data
    "batch_size": 64,         # Higher batch size stabilizes the "noisy" gradients
    "learning_rate": 1e-3, 
    "beta": 0.01,             # Lowered for sharper edges
    "noise_level": 2.0, 
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}
script_dir = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(script_dir, "denoiser_model.pth")
# ============================================
# 1. MODEL
# ============================================
class ConvAutoencoder(nn.Module):
    def __init__(self, latent_dim=CONFIG["latent_dim"]):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, 3, stride=2, padding=1), 
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1), 
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, 7, stride=1, padding=0), 
            nn.ReLU()
        )
        self.fc_mu = nn.Linear(128, latent_dim)
        self.fc_logvar = nn.Linear(128, latent_dim)
        self.fc_decode = nn.Linear(latent_dim + CONFIG["num_classes"], 128) 
        
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, 7, stride=1, padding=0),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1, output_padding=1),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, 3, stride=2, padding=1, output_padding=1),
            nn.Sigmoid()
        )

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x, labels):
        x = x.view(-1, 3, 28, 28)
        h = self.encoder(x).view(-1, 128)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        z = self.reparameterize(mu, logvar)
        
        one_hot = torch.nn.functional.one_hot(labels, num_classes=2).float() * 10.0
        z_cond = torch.cat([z, one_hot], dim=1)
        z_reshaped = self.fc_decode(z_cond).view(-1, 128, 1, 1)
        return self.decoder(z_reshaped).view(-1, 2352), mu, logvar

# ============================================
# 2. BALANCED DATA GENERATOR
# ============================================
def create_fixed_batch(label_list, noise_level=2.0):
    inputs, targets, labels = [], [], []
    for label in label_list:
        img = torch.zeros(3, 28, 28)
        size = torch.randint(6, 12, (1,)).item()
        half_size = size // 2 
        x_c = torch.randint(half_size, 28 - half_size, (1,)).item()
        y_c = torch.randint(half_size, 28 - half_size, (1,)).item()

        color_channel = 0 if label == 0 else 2 
        img[color_channel, y_c-half_size : y_c+half_size, x_c-half_size : x_c+half_size] = 1.0
        
        noise = torch.randn(3, 28, 28) * noise_level
        noisy = torch.clamp(img + noise, 0.0, 1.0)
        
        inputs.append(noisy.view(-1))
        targets.append(img.view(-1))
        labels.append(label)
    return torch.stack(inputs), torch.stack(targets), torch.tensor(labels)

def vae_loss_fn(recon_x, x, mu, logvar):
    BCE = nn.functional.binary_cross_entropy(recon_x, x, reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return BCE + CONFIG["beta"] * KLD

# ============================================
# 3. TRAINING LOOP
# ============================================
def train(model, device):
    optimizer = optim.AdamW(model.parameters(), lr=CONFIG["learning_rate"])
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=100, gamma=0.5)
    # Lower this for a faster startup on laptop CPUs
    print("🎨 Pre-generating 1000 images (Balanced Pool)...")
    all_labels_list = ([0] * 500) + ([1] * 500) 
    
    # This part happens on CPU and is the current "bottleneck"
    p_in, p_targ, p_lab = create_fixed_batch(all_labels_list, CONFIG["noise_level"])
    
    # This moves it to your GTX 965M
    p_in, p_targ, p_lab = p_in.to(device), p_targ.to(device), p_lab.to(device)
    
    model.train()
    print(f"🚀 GPU IS READY: {torch.cuda.get_device_name(0)}")

    dataset_size = len(all_labels_list)
    for epoch in range(CONFIG["epochs"]):
        indices = torch.randperm(dataset_size, device=device)
        
        for i in range(0, dataset_size, CONFIG["batch_size"]):
            batch_idx = indices[i : i + CONFIG["batch_size"]]
            
            inputs = p_in[batch_idx]
            targets = p_targ[batch_idx]
            labels = p_lab[batch_idx]

            optimizer.zero_grad(set_to_none=True)
            output, mu, logvar = model(inputs, labels)
            loss = vae_loss_fn(output, targets, mu, logvar)
            loss.backward()
            optimizer.step()
        scheduler.step()
        
        if epoch % 50 == 0:
            # This saves the model every 50 epochs automatically
            torch.save(model.state_dict(), save_path)
            print(f"💾 Checkpoint saved at epoch {epoch}")
# ============================================
# 4. RUN & TEST
# ============================================
if __name__ == "__main__":
    device = torch.device(CONFIG["device"])
    model = ConvAutoencoder().to(device)
    
    train(model, device)
    torch.save(model.state_dict(), save_path)
    print("✅ Model saved successfully!")
    # Final Stress Test with forced alternating colors
    model.eval()
    test_labels = [0, 1, 0, 1, 0, 1]
    inputs, _, labels = create_fixed_batch(test_labels, noise_level=CONFIG["noise_level"])
    inputs, labels = inputs.to(device), labels.to(device)

    with torch.no_grad():
        outputs, _, _ = model(inputs, labels)
        outputs = (outputs > 0.3).float() # Sharpness threshold

    fig, axes = plt.subplots(6, 2, figsize=(8, 14))
    for i in range(6):
        img_in = inputs[i].cpu().view(3, 28, 28).permute(1, 2, 0).numpy()
        img_out = outputs[i].cpu().view(3, 28, 28).permute(1, 2, 0).numpy()
        axes[i, 0].imshow(img_in); axes[i, 1].imshow(img_out)
        color_name = "RED (0)" if labels[i] == 0 else "BLUE (1)"
        axes[i, 1].set_title(f"AI Guess: {color_name}", color='green')
        axes[i, 0].axis('off'); axes[i, 1].axis('off')

    plt.tight_layout()
    plt.show()
