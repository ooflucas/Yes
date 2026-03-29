import torch
import torch.nn as nn
import torch.optim as optim
class Autoencoder(nn.Module):
    def __init__(self):
        super().__init__()
        
        # ENCODER: 784 → 32
        self.encoder = nn.Sequential(
            nn.Linear(784, 256 ),  # Fill this
            nn.ReLU(),
            nn.Linear(256, 128 ),  # Fill these
            nn.ReLU(),
            nn.Linear(128 , 32)     # Fill input size
        )
        
        # DECODER: 32 → 784  
        self.decoder = nn.Sequential(
            nn.Linear(32, 128 ),   # Fill this
            nn.ReLU(),
            nn.Linear(128, 256),  # Fill these
            nn.ReLU(),
            nn.Linear(256, 784),   # Fill input size
            nn.Sigmoid()           # Keep values 0-1
        )
    
    def forward(self, x):
        encoded = self.encoder(x) 
        decoded = self.decoder(encoded)  # Pass through decoder
        return decoded
model = Autoencoder()
def create_square():
    square = torch.zeros(28, 28)
    square[10:18, 10:18] = 1
    return square.view(-1)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
def learn():
    epoches = 500
    for epoch in range(epoches):
        square = create_square()
        output = model(square)
        loss = criterion(output, square)
