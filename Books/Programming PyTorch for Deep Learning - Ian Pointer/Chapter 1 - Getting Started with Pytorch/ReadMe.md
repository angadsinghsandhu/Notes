# Getting Started with Pytorch

In this chapter we will create our initial uderstandings of PyTorch and how thw API functions. We will also be discussing ways of efficiently using and running these models.

## Building a Custom Deep Learning Machine

The text advises against building a custom machine for deep learning, especially if you're new to it. Instead, the author recommends using `cloud resources` (in either `Amazon Web Services`, `Google Cloud`, or `Microsoft Azure`) and only then start thinking about building your own machine if you feel that you require a single machine for *24/7 operation*.

You do not need to make a massive investment in hardware to run any of the code in this book. If you know your calculations are always going to be restricted to a single machine (with at most a handful of GPUs), it can be cheaper to build a custom rig. However, if your *compute starts to require spanning **multiple** machines and GPUs*, the cloud becomes appealing again. The following sections provide suggestions for what you would need to do so.

### GPU

The GPU is the most important and expensive component in a deep learning box and that the `NVIDIA GeForce RTX 2080 Ti` (considered slow by todays standards) is recommended at the time of writing. For a cheaper option, the `NVIDIA GeForce GTX 1080 Ti` can be used. Although AMD-manufactured GPU cards do exist, their support in PyTorch is currently not good enough to recommend anything other than an NVIDIA card. However, keep a lookout for their `ROCm technology`, which should eventually make them a credible alternative in the GPU space.

### CPU

One should get at least a `Z370 series motherboard` (also considered slow by todays standards). Although many people will tell you that the CPU doesn’t matter for deep learning and that you can get by with a lower-speed CPU as long as you have a powerful GPU, the CPU can become a bottleneck, especially when working with augmented data.

### RAM

It is recommended that a **minimum** of **64GB DDR4** memory for your machine. As more RAM means more batches can be stored in highspeed memory.

### Storage

For storage, an `M2-interface solid-state drive (SSD)` should be installed for your hot data to keep access as fast as possible when you’re actively working on a project. For the second class of storage, add in a `4TB Serial ATA (SATA) drive` for data that you’re not actively working on and transfer to hot and cold storage as required. You can take a look at PCPartPicker to glance at other people’s deep learning machines and get a feel for lists of machine parts and associated prices, which can fluctuate wildly, especially for GPU cards.

## Deep Learning in the Cloud

The text suggests that the cloud option is better for deep learning, especially if you're just starting out. You can shut off the cloud machine and pay pennies for the data being stored in the meantime. You don't need to go all out and use one of `NVIDIA's leviathan Tesla V100 cards` attached to your cloud instance straightaway. You can start out with one of the much cheaper (sometimes even free) `K80-based instances` and move up to the more powerful card when you're ready. The other issue is maintenance. If you get yourself into the good habit of re-creating your cloud instances on a regular basis (ideally starting anew every time you come back to work on your experiments), you'll almost always have a machine that is up to date. If you have your own machine, updating is up to you.

### Google Colaboratory

Google Colaboratory (or Colab), which is a mostly free, **zero-installation-required** custom Jupyter Notebook environment. Colab includes preinstalled versions of TensorFlow and PyTorch, so you don't have to do any setup beyond typing import torch, and every user can get free access to a *NVIDIA T4 GPU for up to 12 hours of continuous runtime*. For free. You can pretty much do every example in this book for nothing with Colab. For that reason, the text recommends using Colab alongside this book to begin with, and then you can decide to branch out to dedicated cloud instances and/or your own personal deep learning server if needed.

### Cloud Providers

Each of the big three cloud providers (Amazon Web Services, Google Cloud Platform, and Microsoft's Azure) offers GPU-based instances (also referred to as `virtual machines or VMs`) and official images to deploy on those instances.

`AWS` offers the `P2` and `P3` instance types to help you out. The `P2` instances use the older **NVIDIA K80 cards** (a maximum of 16 can be connected to one instance), and the P3 instances use the blazing-fast **NVIDIA V100 cards** (and you can strap eight of those onto one instance if you **dare**).

If you're going to use AWS, the text recommends going with the **p2.xlarge** class which will cost you just `90 cents an hour` at the time of this writing and provides plenty of power for working through the examples. You may want to bump up to the P3 classes when you start working on some meaty Kaggle competitions. Remember to shut down your instance when you're not using it! You can do this by right-clicking the instance in the web interface and selecting the Shutdown option.

The text mentions that Google Cloud Platform (GCP) offers K80, P100, and V100-backed instances like Amazon and Azure. In addition to that, GCP offers the aforementioned TPUs for those who have tremendous data and compute requirements.

The charges for Google Cloud should work out to about `70 cents an hour`, making it the cheapest of the three major cloud providers.

### Which Cloud Provider Should I Use?

The text recommends `Google Cloud Platform (GCP)` as the cheapest option and you can scale all the way up to using TPUs if required, with a lot more flexibility than either the AWS or Azure offerings. However, if you have resources on one of the other two platforms already, you'll be absolutely fine running in those environments.

## Using Jupyter Notebook

The text also mentions that Jupyter Notebook is a browser-based environment that allows you to mix live code with text, images, and visualizations and has become one of the de facto tools of data scientists all over the world. Notebooks created in Jupyter can be easily shared. The text also suggests browsing the Jupyter documentation before getting to [Chapter 2](https://github.com/angadsinghsandhu/Notes/tree/master/Books/Programming%20PyTorch%20for%20Deep%20Learning%20-%20Ian%20Pointer/Chapter%202%20-%20Image%20Clasification%20with%20Pytorch) if you've never used it before.

## Installing PyTorch from Scratch

The text explains how to install PyTorch on a Linux server in general. It recommends downloading the appropriate package format for your flavor of Linux and installing the package.

### Download CUDA

Although PyTorch can be run entirely in CPU mode, in most cases, GPU-powered PyTorch is required for practical usage. Assuming you have an NVIDIA card, this is provided by their `Compute Unified Device Architecture (CUDA) API`. The text also recommends installing Anaconda, a packaging system dedicated to producing the best distribution of packages for data scientists.

### Anaconda

The text suggests heading to Anaconda and picking out the installation file for your machine. The text also suggests running `md5sum` on the file you've downloaded and checking it against the list of signatures before executing it with bash `Anaconda3-VERSION-Linux-x86_64.sh` to *make sure that the signature on your machine matches the one on the web page*. This ensures that the downloaded file hasn't been tampered with and means it's safe to run on your system. The script will present several prompts about locations it'll be installing into; unless there's a good reason, just accept the defaults.

### Finally, PyTorch! (and Jupyter Notebook)

The text explains that after installing Anaconda, getting set up with PyTorch is simple: `conda install pytorch torchvision -c pytorch`. This installs PyTorch and the torchvision library that we use in the next couple of chapters to create deep learning architectures that work with images. Anaconda has also installed Jupyter Notebook for us, so we can begin by starting it: jupyter notebook. The text suggests heading to <http://YOUR-IP-ADDRESS:8888> in your browser, creating a new notebook, and entering the following:

```py
import torch
print(torch.cuda.is_available())
print(torch.rand(2,2))
```

This should produce output similar to this:

```py
True
0.6040 0.6647
0.9286 0.4210
[torch.FloatTensor of size 2x2]
```

If `cuda.is_available()` returns `False`, you need to debug your CUDA installation so PyTorch can see your graphics card. The values of the tensor will be different on your instance. The text also explains that tensors are at the heart of almost everything in PyTorch.

## Tensors

The text explains that a <u>***tensor** is both a container for numbers as well as a set of rules that define transformations between tensors that produce new tensors*</u>. It's probably easiest for us to think about tensors as **multidimensional arrays**. Every tensor has a <u>***rank** that corresponds to its dimensional space*</u>. A simple constant scalar (e.g., 1) can be represented as a tensor of **rank 0**, a **vector has a rank 1**, an **n × n matrix has a rank 2**, and so on.

The text also explains that we can create tensors from lists and change an element in a tensor by using standard Python indexing. The text also explains that we can use special creation functions to generate particular types of tensors. In particular, `ones()` and `zeroes()` will generate tensors filled with 1s and 0s, respectively.

The text also explains that we can perform standard mathematical operations with tensors (e.g., adding two tensors together) and <u>if we have a tensor of rank 0, we can pull out the value with `item()`</u>. *Tensors can live in the CPU or on the GPU* and can be copied between devices by using the `to()` function.

### Tensor Operations

Run [basic_pytorch.ipynb](https://github.com/angadsinghsandhu/Notes/blob/master/Books/Programming%20PyTorch%20for%20Deep%20Learning%20-%20Ian%20Pointer/Chapter%201%20-%20Getting%20Started%20with%20Pytorch/basic_pytorch.ipynb) to learn more about Pytorch Tensor operations.

### Tensor Broadcasting

The text explains that borrowed from **NumPy**, broadcasting allows you to perform operations *between a larger and a smaller tensor*. You can broadcast across two tensors if, starting backward from their trailing dimensions: the two dimensions are equal or one of the dimensions is 1.

In our use of broadcasting, it works because 1 has a dimension of 1, and as there are no other dimensions, the 1 can be expanded to cover the other tensor. If we tried to add a [2,2] tensor to a [3,3] tensor, we'd get an error message. But we could add a [1,3] tensor to the [3,3] tensor without any trouble.

Broadcasting is a handy little feature that increases brevity of code and is often **faster** than manually expanding the tensor yourself. That wraps up everything concerning tensors that you need to get started! We'll cover a few other operations as we come across them later in the book, but this is enough for you to dive into Chapter 2.

## Conclusion

The text concludes that whether it's in the cloud or on your local machine, you should now have PyTorch installed. The text has introduced the fundamental building block of the library, the tensor, and you've had a brief look at Jupyter Notebook. This is all you need to get started! In the next chapter, you use everything you've seen so far to start building neural networks and classifying images, so make sure you're comfortable with tensors and Jupyter before moving on.
