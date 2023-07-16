# Image Classification with PyTorch

After setting up PyTorch, we will work through an example that can easily be expanded as you get more comfortable working with PyTorch.

This example is used throughout the book to demonstrate how to debug a model or deploy it to production.

## Our Classification Problem

We will be constructing an *Image Classifier* using a neural network. The network is given a picture and asked to identify what is in the picture.

In this case, you will be building a simple classifier that can tell the difference between `fish` and `cats`, iterating over the design and how you build your model to make it more and more accurate.

## Traditional Challenges

One of the traditional challenges in classification is writing a program that can tell a fish from a cat. One approach could be to write a set of rules describing the characteristics of a cat or a fish. However, this approach would take time, effort, and skill, and could become complicated as more scenarios are encountered.

Deep learning offers an alternative approach by essentially making the computer do all the hard work of constructing all those rules. By creating a <span style="background-color: #FFFF00">structure</span>, giving the network <span style="background-color: #FFFF00">lots of data</span>, and providing it with a way to ==determine whether it is getting the right answer==, <u>***deep learning** can create a function that, given the input of an image, returns cat or fish*</u>. Along the way, we will learn key concepts of how to use PyTorch.

### But First, Data

Before building the image classifier, data is needed. The amount of data required depends on the deep learning technique being used. In this case, training from scratch often requires access to a large quantity of data, so a lot of pictures of *fishes* and *cats* are needed.

One option for obtaining this data is to use a standard collection of images used to train neural networks, called **ImageNet**. It contains more than `14 million images` and `20,000 categories` and is the standard that all image classifiers judge themselves against. Along with the data, PyTorch needs a way to determine what is a cat and what is a fish. This is done using a **label** attached to the data, and training in this manner is called **supervised learning**.

If using ImageNet data, its labels may not be useful because they contain too much information. A label of `tabby cat` or `trout` is separate from `cat` or `fish`, so ==relabeling== may be necessary. A list of image URLs and labels for both fish and cats can be used to download the images from the URLs and place them in the appropriate locations for training (look at [This download.py Script](https://github.com/angadsinghsandhu/Notes/blob/master/Books/Programming%20PyTorch%20for%20Deep%20Learning%20-%20Ian%20Pointer/Chapter%202%20-%20Image%20Clasification%20with%20Pytorch/download.py)).

The relabeling is simple, the `download.py` script stores cat pictures in the directory **train/cat** and fish pictures in **train/fish**. The data now needs to be put into a format that PyTorch can understand.

### PyTorch and Data Loaders

In PyTorch, loading and converting data into formats that are ready for training can often be time-consuming. To make this process more consistent, ==PyTorch has developed standard conventions for interacting with data==, whether it be ==images, text, or audio==. These conventions are **datasets** and **data loaders**.

A <u>***dataset** is a Python class that allows access to the data being supplied to the neural network*</u>. A <u>***data loader** feeds data from the dataset into the network*</u> and can encompass information such as the number of worker processes feeding data into the network or the number of images being passed in at once.

Every dataset, regardless of the type of data it contains, can interact with PyTorch if it satisfies an abstract Python class. This class requires the implementation of two methods: one that returns the size of the dataset i.e. `_len_` and one that retrieves an item from the dataset in a (label, tensor) pair i.e. `_getitem_`. This pair is called by the data loader as it pushes data into the neural network for training.

The `__getitem__` method must be able to take an image and transform it into a tensor, returning both the tensor and the label so that PyTorch can operate on it. While this scenario comes up frequently, PyTorch provides tools to make this process easier.

Here is an example of the ==abstract Python class for a dataset==:

```py
class Dataset(object):
    def __getitem__(self, index):
        raise NotImplementedError
    def __len__(self):
        raise NotImplementedError
```

### Building a Training Dataset

To build a training dataset, the `torchvision` package includes a class called `ImageFolder` that can be used to load images from a directory structure where each directory is a label.

For example, all images labelled as *cat* would be in a directory called `cat`. Here is an example of how to use the `ImageFolder` class to load data for the cats and fish example:

```py
import torchvision
from torchvision import transforms

train_data_path = "./train/"
val_data_path = "./val/"
test_data_path = "./test/"

# creating transformation pipeline
transformation = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def check_image(path):
    try:
        im = Image.open(path)
        return True
    except:
        return False

# getting datasets
train_data = torchvision.datasets.ImageFolder(root=train_data_path, transform=transformation, is_valid_file=check_image)
```

In addition to loading the data, `torchvision` also allows for specifying a list of ==transformations that will be applied to an image before it is fed into the neural network==.

The default transform is to convert image data into a tensor using the `transforms.ToTensor()` method, but other transforms can also be applied.

In this example, incoming images are first scaled to a resolution of 64x64 using the `Resize((64, 64))` transform to increase processing performance.

The images are then converted to tensors and normalized around a specific set of `mean` and `standard deviation` points.

<u>**Normalizing** the data is important because it prevents values from getting too large during the training phase, which can cause the **exploding gradient problem**</u>.

The mean and standard deviation values used in this example are from the ImageNet dataset as a whole, but these values could be calculated specifically for the fish and cat subset if desired.

The ==composable transforms== also allow for easy ==data augmentation== through ==image rotation== and ==skewing==, which will be discussed further in [Chapter 4](https://github.com/angadsinghsandhu/Notes/tree/master/Books/Programming%20PyTorch%20for%20Deep%20Learning%20-%20Ian%20Pointer/Chapter%204%20-%20Transfer%20Learning%20and%20Other%20Tricks).

In addition to the transforms we also specify a `check_image()` function that is passed into aour `ImageFolder API` to cross-check if the path is valid for the images we are loading.

### Building Validation and Test Datasets

In addition to the training data, validation and test datasets are also needed. The difference between these datasets is that :

- The <u>**validation set** is used to evaluate how well the model is generalizing to the problem domain</u>, rather than fitting to the training data.
- The <u>**test set** provides a final evaluation of the model's performance after training is complete</u>.

One danger of deep learning is <u>**overfitting**, where the model becomes very good at recognizing what it has been trained on but cannot generalize to examples it hasn't seen</u>.

To prevent this, a **validation set** of cat and fish pictures that do not occur in the training set is used. At the end of each <u>*training cycle* which is called an **epoch**</u>, the model is compared against this set to make sure it isn't getting things wrong.

In addition to a validation set, we should also create a **test set**. This is used to test the model after all training has been completed.

Here is an example of how to set up the validation and test datasets using the `ImageFolder` class from `torchvision`:

```python
val_data_path = "./val/"
val_data = torchvision.datasets.ImageFolder(root=val_data_path, transform=transformation, is_valid_file=check_image)

test_data_path = "./test/"
test_data = torchvision.datasets.ImageFolder(root=test_data_path, transform=transformation, is_valid_file=check_image)
```

Once the datasets are set up, **data loaders** can be built to feed data from the datasets into the neural network. Here is an example of how to set up data loaders for the training, validation, and test datasets:

```py
# building Data Loaders
batch_size=128
train_data_loader = data.DataLoader(train_data, batch_size=batch_size)
val_data_loader = data.DataLoader(val_data, batch_size=batch_size)
test_data_loader = data.DataLoader(test_data, batch_size=batch_size)
```

The `batch_size` parameter specifies how many images will go through the network before it is trained and updated. Smaller batches, known as `mini-batches`, <u>require less memory and can make training faster by updating the network more quickly</u>.

By default, PyTorch's data loaders are set to a `batch_size` of 1, but this can be changed. The `batch_size` can be adjusted to see ==how big of a mini-batch can be used without exhausting the GPU's memory==. Additional parameters can also be specified, such as how datasets are ==sampled== or whether the entire set is ==shuffled== on each run.

## Finally, a Neural Network

The simplest deep learning network consists of an input layer, which works on the `input tensors`, an `output layer`, which is the size of the number of our output classes (here `2`), and a `hidden layer` between them.

In our first example, we'll use `fully connected layers`. In a <u>**fully connected network**, every node in a layer affects every node in the next layer, and each connection has a **weight** that determines the strength of the signal from that node going into the next layer</u>. These weights are updated when we train the network, normally from a ==random initialization==.

As an input passes through the network, a matrix multiplication of the `weights` and `biases` of that layer onto the input is performed. The result is then passed through an `activation function` to introduce ==nonlinearity== into the system.

Here is an illustration of what a fully connected network with an input layer, a hidden layer, and a two-node output layer:

![Neural Net](https://www.researchgate.net/profile/Haohan-Wang-4/publication/282997080/figure/fig4/AS:305939199610886@1449952997594/A-typical-two-layer-neural-network-Input-layer-does-not-count-as-the-number-of-layers-of.png)

Each connection between nodes ==represents a weight== that determines the strength of the signal from one node to the next.

### Activation Functions

`Activation functions` are used in neural networks to introduce ==nonlinearity== into the system. The most common activation function used in deep learning is the **ReLU**, or **rectified linear unit**. This function is simple, <u>implementing `max(0,x)`, so the result is 0 if the input is negative, or just the input (x) if x is positive</u>.

Another activation function that is commonly used is the **softmax** function. <u>This function produces a set of values between 0 and 1 that adds up to 1, representing probabilities</u>. It weights the values so that it ==exaggerates differences==, producing one result in a vector higher than everything else. The softmax function is ==often used at the **end** of a classification network to ensure that the network makes a definite prediction== about what class it thinks the input belongs to.

### Creating a Network

Creating a network in PyTorch is a very Pythonic affair. We inherit from a class called `torch.nn.Network` and fill out the `__init__` and `forward` methods:

```py
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc1 = nn.Linear(12288, 84)
        self.fc2 = nn.Linear(84, 50)
        self.fc3 = nn.Linear(50,2)

    def forward(self, x):
        x = x.view(-1, 12288)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x))
        return x

simplenet = SimpleNet()
```

In PyTorch, creating a network involves inheriting from the `torch.nn.Module` class and filling out the `__init__` and `forward` methods. The `__init__` method is used to set up the network, such as calling the superclass constructor and defining the layers of the network. The `forward` method describes how data flows through the network during both training and making predictions.

In the example you provided, a simple network called `SimpleNet` is defined with three fully connected layers, called `Linear` in PyTorch. The input data is first converted from a 3D tensor into a 1D tensor of shape **(1, 12288)** (as we are using 64x64 images with 3 RGB channels the total datapoins become 64 x 64 x 3 = **12288**) using the `view()` method so that it can be fed into the first `Linear` layer.

The `relu` activation functions are then applied to the layers in order, with the final `softmax` output providing the **prediction** for that image.

The numbers in the hidden layers are somewhat arbitrary, with the ==exception of the output== of the final layer, which is 2 to match up with the two classes of **cat** or **fish**. In general, it is desirable for the data in the layers to be ==compressed== as it goes down the stack. By reducing the size of the output with respect to the input, that ==part of the network is forced to learn a representation of the original input== with fewer resources, hopefully ==extracting some features== of the images that are important to the problem being solved.

Once a **prediction** has been made, it can be compared with the **actual label** of the original image to see whether it was correct. However, PyTorch needs some way to quantify not just whether a prediction is right or wrong, but just how wrong or right it is.

### Loss Functions

`Loss functions` are an essential component of an effective deep learning solution. PyTorch uses loss functions to <u>determine how to update the network to achieve the desired results</u>.

In the case of a ==multiclass categorization task==, the built-in `CrossEntropyLoss` function is used. Another commonly used loss function is `MSELoss`, which is a standard mean squared loss used for making ==numerical predictions==.

It is important to note that the `CrossEntropyLoss` function incorporates the `softmax()` function as part of its operation. This means that the `forward()` method of the network would need to be updated accordingly.

Here is an example of how the `forward()` method might look after incorporating the `CrossEntropyLoss` function:

```python
def forward(self, x):
    # Convert to 1D vector
    x = x.view(-1, 12288)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)        # No Softmax Applied Here
    return x
```

### Optimizing

Training a neural network involves passing data through the network, using a loss function to determine the difference between the prediction and the actual label, and then using that information to update the weights of the network in an attempt to minimize the loss. To perform these updates, an optimizer is used.

Loss functions can be simple or complex, and PyTorch comes with a comprehensive collection of built-in loss functions that can be used for most applications. In the case of a multiclass categorization task like the one being discussed, the built-in `CrossEntropyLoss` function is recommended. Another commonly used loss function is `MSELoss`, which is a standard mean squared loss used for making numerical predictions.

One thing to be aware of when using the `CrossEntropyLoss` function is that it incorporates the `softmax()` function as part of its operation. This means that the `forward()` method of the network would need to be updated accordingly.

Optimizing a neural network involves finding the lowest point on the `loss curve`, where the loss is ==minimized==. This can be done by altering the values of the weights and checking against the gradient of the curve to determine how good a move is being made.

The size of these moves is known as the `learning rate` and is often a key parameter that needs to be adjusted to get the network learning properly and efficiently. A good learning rate can be determined through experimentation, with a starting value of around ==0.001== often being a good choice. Large learning rates can cause the network to bounce all over the place during training, ==preventing it from converging on a good set of weights==.

![Loss vs Paramerter Graph](https://miro.medium.com/v2/resize:fit:700/1*shYI61ej9RuuqBVHgspDZg.png)

One issue to be aware of when optimizing a neural network is the danger of getting trapped in local minima, where the network appears to have found the shallowest part of the loss curve but actually shallower areas exist elsewhere. To avoid this problem, `stochastic gradient descent (SGD)` can be used, where ==random gradients are sampled during a batch==.

![Loss vs 2 Paramerters Graph](https://www.xpertup.com/wp-content/uploads/2018/05/1-1.gif)

PyTorch comes with several built-in optimizers, including `SGD`, `AdaGrad`, `RMSProp`, and `Adam`. The Adam optimizer is often preferred for deep learning tasks because it uses a ==learning rate per parameter and adapts that learning rate depending on how training is progressing==.

Creating an Adam-based optimizer in PyTorch is simple. The `optim.Adam()` method is called and passed the weights of the network that it will be updating, along with the desired learning rate. Here is an example of how to create an Adam-based optimizer for the `SimpleNet` network with a learning rate of 0.001:

```python
import torch.optim as optim
optimizer = optim.Adam(simplenet.parameters(), lr=0.001)
```

## Training

Training a neural network involves `passing data through the network`, `using a loss function to determine the difference between the prediction and the actual label`, and then `using an optimizer to update the weights of the network in an attempt to minimize the loss`.

The code trains a PyTorch model by iterating over each epoch and each batch of data within each epoch. For each batch, it computes the model's predictions, computes the loss between these predictions and the true targets, computes gradients with respect to this loss, and updates the model's parameters using these gradients. It also keeps track of training loss by accumulating it over all batches and computing its average at end of each epoch.

Then the code evaluates a trained PyTorch model by iterating over each batch of validation data. For each batch, it computes the model’s predictions, computes the loss between these predictions and the true targets, and updates some statistics such as validation loss and accuracy. At end of each epoch, it prints out these statistics.

Here is an example of a complete training loop that combines everything we've discussed so far:

```python
def train(model, optimizer, loss_fn, train_loader, val_loader, epochs=20, device="cpu"):
    for epoch in range(1, epochs+1):
        # part 1 : Training
        model.train()
        train_loss = 0.0

        for batch in train_loader:
            optimizer.zero_grad()
            inputs, targets = batch

            inputs = inputs.to(device)
            targets = targets.to(device)

            output = model(inputs)
            loss = loss_fn(output, targets)
            loss.backward()
            optimizer.step()

            train_loss += loss.data.item()

        train_loss /= len(train_loader.dataset)

        # Part 2 : Evaluation
        model.eval()
        val_loss = 0.0

        num_correct = 0
        num_examples = 0

        for batch in val_loader:
            inputs, targets = batch

            inputs = inputs.to(device)
            targets = targets.to(device)

            output = model(inputs)
            loss = loss_fn(output, targets)

            val_loss += loss.data.item() * inputs.size(0)
            
            correct = torch.eq(torch.max(F.softmax(output, dim=1), dim=1)[1], targets)
            num_correct += torch.sum(correct).item()
            num_examples += correct.shape[0] 

        val_loss /= len(val_loader.dataset)

        # printing statememnt per epoch
        print(f"Epoch: {epoch}, Training Loss: {train_loss:.4f}, Validation Loss: {val_loss:.3f}, Accuracy: {(num_correct/num_examples):.2f}")
```

`def train(model, optimizer, loss_fn, train_loader, val_loader, epochs=20, device="cpu"):` This line defines the function `train` and its parameters. The function takes in the following arguments:

- `model`: The PyTorch model to be trained.
- `optimizer`: The optimizer used to update the model's parameters.
- `loss_fn`: The loss function used to compute the loss between the model's predictions and the true targets.
- `train_loader`: A PyTorch DataLoader object that provides batches of training data.
- `val_loader`: A PyTorch DataLoader object that provides batches of validation data.
- `epochs`: The number of epochs to train the model for. An epoch is one complete pass through the entire training dataset. This parameter is optional and has a default value of 20.
- `device`: The device on which to perform the computations. This parameter is optional and has a default value of "cpu".

We iterate over each epoch using `for epoch in range(1, epochs+1):`. We first initialize the `train_loss` float variables as **0.0** which is used to keep track of the training loss.

Every `Epoch` has 2 parts, the ==train== part and the ==evaluation== part. We start the Train part of the epoch by calling `model.train()`. This line sets the model to training mode. In ==training mode==, certain layers of the model such as `dropout` and `batch normalization` behave differently than in ==evaluation mode==.

We then start looping over every batch created by our data loader, specifically our Data Loader for Training. This is done by calling `for batch in train_loader:`. The next command `optimizer.zero_grad()` method is called at the beginning of ==each iteration== to ==reset the gradients to zero==. This is necessary because gradients accumulate by default, meaning that if they were not reset, each batch would have to deal with the gradients from all previous batches as well as its own.

We unpack the current batch of data into inputs and targets by calling `inputs, targets = batch`. Then move the inputs and targets to the specified device (CPU or GPU) using the `.to()` API as `inputs = inputs.to(device)` and `targets = targets.to(device)`.

This line We computes the model's predictions for the current batch of inputs, by passing the inputs to the model as a parameter: `output = model(inputs)`.

`loss = loss_fn(output, targets)`: This line computes the loss between the ==model's predictions== and the ==true targets== using the provided loss function. After the loss is calculated we compute the gradients of all optimized parameters with respect to the loss by calling `loss.backward()` (Backward Propogation). Finally the command `optimizer.step()` updates the model's parameters using the newly computed gradients using the optimizer.

First `train_loss += loss.data.item()` adds the current batch's loss to the running total of training loss for the epoch. Then, `train_loss /= len(train_loader.dataset)` computes the ==average== training loss over all batches by dividing the **total training loss** by **the size of the training dataset**.

This is where the first part i.e. Training Mode of the epoch ends. Now we begin the Evaluation Mode of the epoch. `model.eval()`: is called to set the model to evaluation mode. In evaluation mode, certain layers of the model such as dropout and batch normalization behave differently than in training mode.

Similar to the `train_loss` float variable we initialize the `val_loss` float as **0.0**. This variable will be used to keep track of the validation loss.

We also initialize the variables `num_correct` and `num_examples` to 0. These variables will be used to keep track of the ==number of correct predictions== and the ==total number of examples==, respectively.

Similar to the Training Mode, Now we start a for loop that will iterate over each batch of data provided by the `val_loader` through `for batch in val_loader:`. The line `inputs, targets = batch` unpacks the current batch of data into inputs and targets. `inputs = inputs.to(device)` and `targets = targets.to(device)` are used to move the inputs and targets to the specified device. `output = model(inputs)` computes the model's predictions for the current batch of inputs. `loss = loss_fn(output, targets)` computes the loss between the ==model's predictions== and the ==true targets== using the provided loss function.

The line `val_loss += loss.data.item() * inputs.size(0)` updates the running total of validation loss. The `loss.data.item()` expression extracts the scalar value of the loss computed for the current batch of data. This value is then multiplied by the size of the current batch, `inputs.size(0)`, to weight the contribution of this batch's loss to the total validation loss (this step is no required if all batches are of same size but it is still a good convention to have). This weighting is necessary because the last batch of data may be smaller than the other batches if the size of the validation dataset is not divisible by the batch size.

In other words, this line computes a weighted average of the losses over all batches of validation data, where each batch's loss is weighted by the size of the batch. This ensures that the computed validation loss is an unbiased estimate of the average loss over the entire validation dataset, even if the batch sizes are not all equal.

Then the line `correct = torch.eq(torch.max(F.softmax(output, dim=1), dim=1)[1], targets)` computes a boolean tensor indicating which predictions are correct. The `F.softmax(output, dim=1)` expression applies the softmax function to the model's predictions along the second dimension (i.e., across the classes, the first dim being a particular sample in the batch) to obtain a probability distribution over the classes for each example in the batch. The `torch.max(..., dim=1)` expression then computes the maximum probability and its corresponding class index for each example. The `[1]` indexing operation extracts the class indices corresponding to the maximum probabilities.

The `torch.eq(..., targets)` expression then compares these predicted class indices to the true class indices provided in `targets`. This returns a boolean tensor of the same shape as `targets`, where each element is `True` if the corresponding prediction is correct and `False` otherwise. This boolean tensor is then assigned to the variable `correct`. In other words, this line computes a boolean mask indicating which examples in the current batch were correctly classified by the model.

Finally, `num_correct += torch.sum(correct).item()` adds the ==number of correct predictions in the current batch== to the ==running total of correct predictions==. And `num_examples += correct.shape[0]` adds the ==size of the current batch== to the ==running total of examples==.

We computes the ==average validation loss over all batches== by dividing the ==total validation loss== by the ==size of the validation dataset== i.e. `val_loss /= len(val_loader.dataset)`.

The last line prints out some statistics for each epoch, including training loss, validation loss, and accuracy.

### Making It Work on the GPU

To take advantage of the GPU, we need to move our input tensors and the model itself to the GPU by explicitly using the `to()` method. Here’s an example that copies the `SimpleNet` to the GPU:

```python
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model.to(device)
```

In this example, the model is copied to the GPU if PyTorch reports that one is available, or otherwise kept on the CPU. By using this construction, we can determine whether a GPU is available at the start of our code and use `tensor.to(device)` or `model.to(device)` throughout the rest of the program, being confident that it will go to the correct place.

## Putting It All Together

[ch2 Jupyter Notebook](https://github.com/angadsinghsandhu/Notes/blob/master/Books/Programming%20PyTorch%20for%20Deep%20Learning%20-%20Ian%20Pointer/Chapter%202%20-%20Image%20Clasification%20with%20Pytorch/ch2.ipynb)

### Making Predictions

Once a neural network has been trained, it can be used to make predictions. Here is an example of how to use the `SimpleNet` network to generate a prediction for a single image:

```python
labels = ['cat','fish']

img = Image.open("./val/fish/100_1422.JPG") 
img = transformation(img).to(device)
img = torch.unsqueeze(img, 0)

simplenet.eval()
prediction = F.softmax(simplenet(img), dim=1)
prediction = prediction.argmax()
print(labels[prediction]) 
```

In this example, an image is loaded from the filesystem and transformed using the ==same transform pipeline== that was used during training. Because the network expects a 4D tensor representing a batch of images, <u>the image tensor is expanded to add an extra dimension at the front using the</u> `unsqueeze(0)` method.

The image is then passed through the model to generate a prediction. The `argmax()` function is used to find the index of the highest value in the prediction tensor, which corresponds to the predicted class. This index is then used to look up the corresponding label in the `labels` array and print out the prediction.

We ould calculate the ==Accuracy== of our tained model on the Test Set (Data that the model has never seen before) by using the following code:

```py
labels = ['cat','fish']
correct = 0
total = 0

with torch.no_grad():
    for batch in test_data_loader:
        inputs, targets = batch
        inputs = inputs.to(device)
        targets = targets.to(device)

        predictions = simplenet(inputs)

        for i, prediction in enumerate(predictions):
            prediction = prediction.argmax()
            if prediction == targets[i]:
                correct += 1
            total += 1
        
        accuracy = correct / total
        print(f"Accuracy of this Batch {i+1} : {accuracy}")
```

`labels = ['cat','fish']` defines a list of class labels. In this case, there are two classes: 'cat' and 'fish'. `correct = 0` and `total = 0` initialize the variables `correct` and `total` to 0. These variables will be used to keep track of the number of correct predictions and the total number of examples, respectively. `with torch.no_grad():` command starts a `with` block that ==disables gradient computation==. Since we are ==only evaluating== the model and ==not updating== its parameters, we do not need to compute gradients.

`for batch in test_data_loader:`: starts a for loop that will iterate over each batch of data provided by the `test_data_loader`. `inputs, targets = batch` unpacks the current batch of data into inputs and targets. The lines `inputs = inputs.to(device)` and `targets = targets.to(device)` move the inputs and targets to the specified device.

We compute the model's predictions for the current batch of inputs using `predictions = simplenet(inputs)`. We start a nested for loop to iterate over each example in the current batch i.e. `for i, prediction in enumerate(predictions):`.

`prediction = prediction.argmax()` computes the index of the maximum value in the prediction vector for the current example. This index corresponds to the predicted class for this example. We check if the predicted class for this example is equal to its true class, If the predicted class is equal to the true class, then we increment the variable `correct` by 1 to count this as a correct prediction `if prediction == targets[i]: correct += 1`.

`total += 1` increments the variable `total` by 1 to count this example. After all examples in all batches have been processed, `accuracy = correct / total` computes the overall accuracy by dividing the number of correct predictions by the total number of examples. The last line prints out some statistics for each batch, including its accuracy.

### Model Saving

In PyTorch, you can save the current state of a model in Python's pickle format by using the `torch.save()` method. Conversely, you can load a previously saved iteration of a model by using the `torch.load()` method.

Here is an example of how to save the current parameters and model structure of the `SimpleNet` model to a file:

```python
torch.save(simplenet, "/tmp/simplenet")
```

To reload the saved model, you can use the `torch.load()` method as follows:

```python
simplenet = torch.load("/tmp/simplenet")
```

This stores both the parameters and the structure of the model to a file. However, if you change the structure of the model at a later point, this might cause problems. For this reason, it is more common to save a model's `state_dict` instead. The `state_dict` is a standard Python dictionary that contains maps of each layer's parameters in the model.

Here is an example of how to save the `state_dict` of a model:

```python
torch.save(model.state_dict(), PATH)
```

To restore the `state_dict`, you first need to create an instance of the model and then use the `load_state_dict()` method. Here is an example of how to do this for the `SimpleNet` model:

```python
simplenet = SimpleNet()
simplenet_state_dict = torch.load("/tmp/simplenet")
simplenet.load_state_dict(simplenet_state_dict)
```

The benefit of using the `state_dict` is that it allows for more flexibility when extending or modifying the model. The `load_state_dict()` method can be called with a `strict=False` parameter to assign parameters to layers in the model that exist in the `state_dict`, but does not fail if the loaded `state_dict` has layers missing or added from the model's current structure.

Models can be saved to disk during a training run and reloaded at another point so that training can continue where it left off. This can be useful when using cloud-based GPU resources that have time limits, as it allows you to save the model before reaching the time limit and continue training in a new session.

## Conclusion

In this chapter, you have learned the basics of neural networks and how to train them with a dataset, make predictions on other images, and save/restore models to and from disk using PyTorch.

Before moving on to the next chapter, you can experiment with the `SimpleNet` architecture by adjusting the number of parameters in the `Linear` layers, adding more layers, or trying out different activation functions. You can also see how training is affected by adjusting the learning rate, switching out the optimizer, or changing the batch size and initial size of the image.

A lot of deep learning work involves tinkering with these parameters by hand until a network is trained appropriately, so it's good to get a handle on how all the moving parts interact. While the accuracy of the `SimpleNet` architecture may not be as high as desired, don't worry! [Chapter 3](https://github.com/angadsinghsandhu/Notes/tree/master/Books/Programming%20PyTorch%20for%20Deep%20Learning%20-%20Ian%20Pointer/Chapter%203%20-%20Convolutional%20Neural%20Networks) introduces `convolutional neural networks`, which provide definite improvements over the simple network used so far.
