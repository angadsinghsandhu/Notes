import torch
from datetime import datetime as dt
from train.gpt import GPTLanguageModel, estimate_loss, get_batch, decode

# hyperparameters
max_iters = 5000
eval_interval = 500
learning_rate = 3e-4
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# ------------

# # hyperparameters low
# max_iters = 2500
# eval_interval = 250
# learning_rate = 3e-4
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# # ------------

def train_gpt():
    model = GPTLanguageModel()
    print("...")
    m = model.to(device)
    # print the number of parameters in the model
    print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

    # create a PyTorch optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    for iter in range(max_iters):

        # every once in a while evaluate the loss on train and val sets
        if iter % eval_interval == 0 or iter == max_iters - 1:
            losses, model = estimate_loss(model)
            print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

        # sample a batch of data
        xb, yb = get_batch('train')

        # evaluate the loss
        logits, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    # getting current time string
    timestamp = dt.now().strftime("_%Y_%m_%d-%H_%M")

    # saving model
    torch.save(m.state_dict(), f"gpt_state{timestamp}.pt")

def generate_gpt():
    # loading model
    m = GPTLanguageModel()
    m.load_state_dict(torch.load("model/gpt_state.pt", map_location=device))
    m.eval()

    # generate from the model
    context = torch.zeros((1, 1), dtype=torch.long, device=device)
    print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))
    # open('./data/sample_output.txt', 'w').write(decode(m.generate(context, max_new_tokens=10000)[0].tolist()))