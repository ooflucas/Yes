import torch
import torch.nn as nn
que = [10.5, 2.72, 30.92]
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(2, 1)
    def forward(self, x):
    	return self.layer(x)
X = torch.tensor([[1.0, 3.0], [2.0, 5.0], [3.0, 1.0]], dtype=torch.float32)
Y = torch.tensor([[4.1], [6.8], [10.2]], dtype=torch.float32)
test_tensor = torch.tensor([[que[0]], [que[1]], [que[2]]], dtype=torch.float32)
model = Model()
def ans_cal():
	ans = []
	for dis1 in que:
		ans.append(dis1*3+1)
	return ans
optimizer = torch.optim.Adam(model.parameters(), lr=0.1)
def train(epochs):
	criterion = nn.MSELoss()
	for epoch in range(epochs):
		optimizer.zero_grad()
		pred = model(X)
		loss = criterion(pred, Y)
		grad = loss.backward()
		optimizer.step()
		if epoch % 100 == 0:
			print(f'epoch{epoch} loss: {loss}')
ans1 = ans_cal()
train(5000)
model.eval() 
with torch.no_grad():
	predictions = model(test_tensor)
	print("AI's Predicted Prices:")
	print(predictions)
	print("\nActual Target Prices:")
	print(ans1
