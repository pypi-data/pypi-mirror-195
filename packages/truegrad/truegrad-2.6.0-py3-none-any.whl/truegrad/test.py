import datetime
import torch
import optim
import time
from lion_pytorch import Lion
import copy
from matplotlib import pyplot as plt

numbers = 16
features = 2 ** 12
depth = 0
input_scale = 1
lr = 1e-3
iterations = 2**9
noise_scale_range = list(range(-1, -3, -1))
batch_size = 2**18
offset = 4
printervall = 8

a = torch.nn.Sequential(torch.nn.Linear(numbers, features), torch.nn.ReLU(), torch.nn.LayerNorm(features),
                        *[layer for _ in range(depth) for layer in [torch.nn.Linear(features, features), torch.nn.ReLU(), torch.nn.LayerNorm(features, features)]],
                        torch.nn.Linear(features, 1)).cuda()
plt.yscale("log")
plt.xscale("log")
start_time = datetime.datetime.now()
colors = [lambda x: f"#{x:02x}0000", lambda x: f"#00{x:02x}00", lambda x: f"#0000{x:02x}", lambda x: f"#{x:02x}{x:02x}00", lambda x: f"#{x:02x}00{x:02x}", lambda x: f"#00{x:02x}{x:02x}"]

noise_scale = None


def get_noise():
    inp = torch.randn((batch_size, numbers), device="cuda:0") * input_scale
    noise = torch.randn_like(inp) * inp.std() * noise_scale
    return inp, noise



def noisy_square():
    inp, noise = get_noise()
    target = (noise + inp.square())
    ground_truth = inp.square()
    return inp, target, ground_truth


def rosenbrock(x, y):
    return (1 - x).square() + 100 * (y - x.square()).square()

def noisy_rosenbrock():
    inp, noise = get_noise()
    target = rosenbrock(*(inp + noise).chunk(2, 1))
    ground_truth = rosenbrock(*inp.chunk(2, 1))
    return inp, target, ground_truth

example = noisy_rosenbrock

criterion = torch.nn.functional.l1_loss


for sc_idx, scale in enumerate(noise_scale_range):
    noise_scale = 2 ** scale
    all_losses = []

    aa = [copy.deepcopy(a) for _ in range(6)]
    oo = [torch.optim.Adam(aa[0].parameters(), lr=lr),
          optim.Graft(aa[1].parameters(), torch.optim.Adam(aa[1].parameters(), lr=lr), Lion(aa[1].parameters(), lr=1), weight_decay=0),
          optim.Graft(aa[2].parameters(), torch.optim.Adam(aa[2].parameters(), lr=lr), torch.optim.SGD(aa[2].parameters(), lr=1), weight_decay=0),
          optim.Graft(aa[3].parameters(), torch.optim.SGD(aa[3].parameters(), lr=lr), torch.optim.Adam(aa[3].parameters(), lr=1), weight_decay=0),
          optim.Sign(aa[4].parameters(), torch.optim.Adam(aa[4].parameters(), lr=lr), lr),
          optim.Sign(aa[5].parameters(), torch.optim.Adam(aa[5].parameters(), lr=lr))]

    for i in range(iterations):
        losses = []
        inp, target, ground_truth = example()
        target = target.mean(-1, keepdim=True)
        ground_truth = ground_truth.mean(-1, keepdim=True)
        for a, o in zip(aa, oo):
            out = a(inp)
            criterion(out, target).backward()
            o.step()
            o.zero_grad()
            with torch.no_grad():
                losses.append(criterion(out, ground_truth).detach().to(device="cpu", non_blocking=True))
        all_losses.append(losses)
        if i % printervall == offset:
            print(f'{sc_idx} | {i:06d} | {datetime.datetime.now() - start_time} | {datetime.datetime.now()} | {" - ".join(f"{o.item():10.2f}" for o in all_losses[-offset])}')

    all_losses = [[i.item() for i in losses] for losses in all_losses]
    skipped = len(all_losses) // 32
    for i, (name, ls) in enumerate(zip(["Adam#Adam", "Adam#Lion", "Adam#SGD", "SGD#Adam", "SGD#SignAdam", "Adam#SignAdam"], zip(*all_losses))):
        color = colors[i](round(255 - 128 * sc_idx / len(noise_scale_range)))
        plt.plot(list(range(skipped, len(ls))), [sum(ls[i:i+skipped]) / skipped for i in range(len(ls) - skipped)], color=color, label=f"{name} - noise_scale=2**{scale}")
plt.legend()
plt.show()

