import torch
import numpy as np
import torch.nn as nn
# Create a 26x26 matrix where each row is a one-hot vector
encoding_matrix = np.eye(26, dtype=int)
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(26, 26)
    def forward(self, x):
        return self.layer(x)
X = torch.tensor(np.array([
    encoding_matrix[19],
    encoding_matrix[0],
    encoding_matrix[23]
]), dtype=torch.float32)
Y = torch.tensor(np.array([
    encoding_matrix[0],
    encoding_matrix[23],
    encoding_matrix[8]
]), dtype=torch.float32)
test_tensor = torch.tensor(np.array([
    encoding_matrix[19],
    encoding_matrix[0],
    encoding_matrix[23]
]), dtype=torch.float32)
model = Model()
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
def train(epochs):
    criterion = nn.MSELoss()
    for epoch in range(epochs):
        optimizer.zero_grad()
        pred = model(X)
        loss = criterion(pred, Y)
        loss.backward()
        optimizer.step()
        if epoch % 100 == 0:
            print(f'epoch{epoch} loss: {loss}')
train(500)
model.eval()
with torch.no_grad():
    pred = model(test_tensor)
    predicted_indices = torch.argmax(pred, dim=1)
    predicted_letters = [chr(index + 97) for index in predicted_indices]
    word = "".join(predicted_letters)
    print(f"Indices: {predicted_indices}")
    print(f"Predicted Word: {word}")