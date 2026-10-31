def mlp(inputs, outputs, width):
    layers = []
    for n in (inputs, width, width):
        layers.extend((nn.Linear(n, width), nn.LeakyReLU(.2)))
    layers.append(nn.Linear(width, outputs))
    return nn.Sequential(*layers)

class RoutedMLP(nn.Module):
    """Every input uses the same softmax route at train and inference time."""
    def __init__(self, inputs, outputs, z_dim=4, width=48, router_width=16):
        super().__init__()
        self.router = mlp(inputs, z_dim, router_width)
        self.net = mlp(inputs + z_dim, outputs, width)

    def forward(self, x, particles):
        q = self.router(x)
        weights = (q @ particles.T / math.sqrt(particles.shape[1])).softmax(-1)
        z = weights @ particles
        return self.net(torch.cat((x, z), dim=-1))
