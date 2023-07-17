# Convolutional Neural Networks

After experimenting with **fully connected neural networks** in Chapter 2, you may have noticed some limitations. Adding more layers or increasing the number of parameters may have caused you to run out of memory on your GPU. Additionally, training the network to achieve decent accuracy took a long time and the results were not as impressive as expected from deep learning.

Fully connected networks can function as *universal approximators*, but the theory does not specify how long it will take to train them to approximate the desired function. However, there is a better approach for working with images: **Convolutional Neural Networks (CNNs)**. CNNs form the backbone of the most accurate image classifiers today and are quicker to train and more accurate than fully connected networks.

In this chapter, you will learn about CNNs and how to build a new convolutional-based architecture for your fish versus cat application. This new architecture will be quicker to train and more accurate than the approach used in the previous chapter.

## Our First Convolutional Model

In this chapter, the author shares the final model architecture first and then discusses all the new pieces. The training method created in Chapter 2 is independent of the model, so you can test this model out first and then come back for the explanation.

One new feature introduced in this chapter is the use of `nn.Sequential()`, which allows you to create a chain of layers. When using one of these chains in `forward()`, the input goes through each element of the array of layers in succession. This can be used to break your model into more logical arrangements. In this network, there are two chains: the features block and the classifier.

The `Conv2d` layer is also introduced in this chapter. This layer performs a 2D convolution on the input data and is commonly used in image classification tasks. By using `nn.Sequential()` and `Conv2d`, you can build a powerful CNN architecture for your application.

### Convolutions

The `Conv2d` layer is a 2D convolution that operates on a grayscale image. A grayscale image consists of an array of pixels, with each pixel having a value that indicates its color. For example, an 8-bit image can have pixel values ranging from 0 to 255.

To perform the convolution, a filter or convolutional kernel is passed over the image. This filter is typically smaller than the image and is dragged across the image to produce an output or feature map. For example, consider a small, square image that is 4 pixels high and wide and a 2x2 filter. To produce the output, the filter is passed over the original input like a magnifying glass over a piece of paper.

Starting from the top left, the first calculation multiplies each element in the filter by its corresponding element in the image and sums the result. For example, if the first four pixels of the image have values 10, 11, 2, and 123 and the filter has values 1, 0, 1, and 0, then the first calculation would be (10 x 1) + (11 x 0) + (2 x 1) + (123 x 0) = 12.

After this calculation is performed, the filter is moved across by a certain amount (in this case, by 2) and the calculation is repeated. This process continues until the entire image has been covered by the filter. The final result is a feature map that represents the output of the convolution.

In summary, the `Conv2d` layer performs a 2D convolution on a grayscale image by passing a filter over the image and performing calculations at each position. This produces a feature map that can be used for further processing in a CNN architecture.

A convolutional layer can have many filters, the values of which are determined during the training of the network. All the filters in the layer share the same bias values. The `Conv2d` layer is invoked with several options that can be set: `in_channels`, `out_channels`, `kernel_size`, `stride`, and `padding`.

The `in_channels` parameter specifies the number of input channels received in the layer. At the beginning of the network, an RGB image is taken as input, so the number of input channels is three. The `out_channels` parameter specifies the number of output channels, which corresponds to the number of filters in the conv layer. The `kernel_size` parameter describes the height and width of the filter and can be a single scalar specifying a square or a tuple for a non-square filter.

The `stride` parameter indicates how many steps across the input to move when adjusting the filter to a new position. This can have a big effect on the downstream layers of your network and even what that particular layer ends up looking at. The `padding` parameter specifies how to handle edge cases when performing the convolution. If padding is not set, any edge cases encountered in the last columns of the input are simply thrown away. It's up to you to set padding appropriately.

In summary, by invoking the `Conv2d` layer with appropriate options, you can build a powerful CNN architecture for your application.

### Pooling

Pooling layers are often used in conjunction with convolutional layers in a CNN architecture. These layers reduce the resolution of the network from the previous input layer, resulting in fewer parameters in lower layers. This compression leads to faster computation and helps prevent overfitting in the network.

In the model described in the text, `MaxPool2d` is used with a kernel size of 3 and a stride of 2. This means that for an input of size 5x3, two 3x3 tensors are generated by the pooling operation. In `MaxPool`, the maximum value is taken from each of these tensors, resulting in an output tensor of [6,9]. There is also a padding option in `MaxPool` that creates a border of zero values around the tensor in case the stride goes outside the tensor window.

Aside from taking the maximum value, other functions can be used for pooling. A popular alternative is to take the average of the tensor values, allowing all of the tensor data to contribute to the pool instead of just one value in the max case. PyTorch also provides `AdaptiveMaxPool` and `AdaptiveAvgPool` layers, which work independently of the incoming input tensor's dimensions. These adaptive pooling layers are recommended for use in model architectures because they allow you to create architectures that can work with different input dimensions.

In summary, pooling layers are used in CNN architectures to reduce the resolution of the network and prevent overfitting. Different pooling functions and options can be used to achieve different results.

### Dropout

Dropout is a technique used in neural networks to prevent overfitting to training data. It works by randomly ignoring a certain percentage of nodes within the network during a training cycle. This means that these nodes won't be updated and won't have the chance to overfit to the input data. Because the selection of ignored nodes is random, each training cycle will ignore a different selection of the input, which should help generalization even further.

In the example CNN network described in the text, the Dropout layers are initialized with a value of 0.5, meaning that 50% of the input tensor is randomly zeroed out. This value can be changed by adding the `p` parameter to the initialization call, for example `Dropout(p=0.2)` to set the dropout rate to 20%.

It's important to note that Dropout should only take place during training and not during inference. If Dropout was happening during inference, a chunk of the network's reasoning power would be lost, which is not desirable. PyTorch's implementation of Dropout automatically determines which mode the network is running in and passes all data through the Dropout layer at inference time.

In summary, Dropout is a simple and effective technique for preventing overfitting in neural networks by randomly ignoring a certain percentage of nodes during training.

### BatchNorm

BatchNorm, short for batch normalization, is a layer that helps ensure that each minibatch that goes through the network has a mean centered around zero with a variance of 1. This is achieved using two learned parameters that are trained along with the rest of the network. BatchNorm can be useful for larger networks, where the effect of any layer on another can be vast due to repeated multiplication. This can result in vanishing or exploding gradients, which are fatal to the training process. BatchNorm helps prevent this by making sure that the multiplications inside the network don't get out of hand.

Even if BatchNorm is used in a network, it is still recommended to normalize the input data using a transformation chain, as was done in Chapter 2. This is because it will take longer for the network to learn how to get the inputs under control if they are not already normalized. Normalizing the input data can help speed up the training process.

You can instantiate all of the architectures discussed so far and use `print(model)` to see which layers they use and in what order operations happen. This can help you understand how BatchNorm and other layers work together in a CNN architecture.

## History of CNN Architectures

CNN models have been around for decades, with LeNet-5 being used for digit recognition on checks in the late 1990s. However, it wasn't until GPUs became widely available that deep CNN networks became practical. In the last seven years, deep learning networks have started to outperform all other existing approaches in image classification.

### AlexNet

One of the most influential CNN architectures is AlexNet, which was released in 2012 and won that year's ImageNet competition with a top-5 error rate of 15.3%. AlexNet introduced the concepts of MaxPool and Dropout and popularized the ReLU activation function. It was one of the first architectures to demonstrate that many layers were possible and efficient to train on a GPU. Although it's not state-of-the-art anymore, AlexNet remains an important milestone in deep learning history.

Interestingly, the network that has been used in this chapter so far is actually based on the AlexNet architecture. This is why standard MaxPool2d was used instead of AdaptiveMaxPool2d, to match the original AlexNet definition.

### Inception/GoogLeNet

The winner of the 2014 ImageNet competition was the GoogLeNet architecture, which introduced the Inception module to address some of the deficiencies of AlexNet. In AlexNet, the kernels of the convolutional layers are fixed at a certain resolution, which may not be optimal for detecting details at both macro- and microscales. For example, determining whether an object is a car may require a large kernel, while determining its specific model may require a smaller kernel to make out details such as logos and insignias.

The Inception network addresses this issue by running a series of convolutions of different sizes on the same input and concatenating all of the filters together to pass on to the next layer. Before doing this, it performs a 1x1 convolution as a bottleneck that compresses the input tensor, allowing the 3x3 and 5x5 kernels to operate on fewer filters than they would if the 1x1 convolution wasn't present.

The original GoogLeNet architecture uses nine Inception modules stacked on top of each other, forming a deep network. Despite its depth, it uses fewer parameters overall than AlexNet while delivering a human-like performance with a top-5 error rate of 6.67%.

In summary, the GoogLeNet architecture introduced the Inception module, which uses multiple convolutional kernels of different sizes to detect details at different scales in an image. This allows for more effective feature extraction and improved performance in image classification tasks.

### VGG

Another influential CNN architecture is the VGG network, which was the second-place entry in the 2014 ImageNet competition. Developed by the Visual Geometry Group at the University of Oxford, the VGG network is a simpler stack of convolutional layers that comes in various configurations. In its VGG-16 configuration, it achieved an 8.8% top-5 error rate.

The downside of the VGG approach is that its final fully connected layers make the network very large, with 138 million parameters compared to GoogLeNet's 7 million. Despite its size, the VGG network remains popular in the deep learning world due to its simpler construction and early availability of trained weights. It is often used in style transfer applications because its combination of convolutional filters can capture information in a way that is easier to observe than more complex networks.

In summary, both GoogLeNet and VGG are influential CNN architectures that have achieved impressive results in image classification tasks. Each has its own strengths and weaknesses, and their use depends on the specific application and requirements.

### ResNet

ResNet, developed by Microsoft, is another influential CNN architecture that won the ImageNet 2015 competition with a top-5 score of 4.49% in its ResNet-152 variant and 3.57% in an ensemble model. The innovation that ResNet brought was an improvement on the Inception-style stacking bundle of layers approach. In ResNet, each bundle performs the usual CNN operations but also adds the incoming input to the output of the block.

The advantage of this setup is that each block passes through the original input to the next layer, allowing the "signal" of the training data to traverse through deeper networks than possible in either VGG or Inception. This helps prevent the loss of weight changes in deep networks, known as a vanishing gradient, where the gradient changes in backpropagation tend to zero during the training process.

In summary, ResNet is a powerful CNN architecture that introduced an improved stacking bundle of layers approach to achieve impressive results in image classification tasks. By adding the incoming input to the output of each block, ResNet allows for deeper networks and helps prevent vanishing gradients during training.

### Other Architectures Are Available

Since 2015, many other CNN architectures have been developed that have incrementally improved accuracy on ImageNet. Some examples include DenseNet, which extends the ResNet idea to allow for the construction of very deep networks, and SqueezeNet and MobileNet, which offer reasonable accuracy while being much smaller than architectures such as VGG, ResNet, or Inception.

Another area of research is using neural networks to design other neural networks. Google's AutoML system has been successful in this area, generating architectures such as NASNet and PNAS that achieve state-of-the-art results on ImageNet. In fact, the organizers of the ImageNet competition have decided to stop holding further competitions because the architectures have already surpassed human levels of ability.

In summary, there are many powerful CNN architectures available that can be used for image classification tasks. These architectures range from very deep and complex to small and efficient, and new architectures are being developed all the time.

## Using Pretrained Models in PyTorch

PyTorch provides many popular models by default in the torchvision library, making it easy to use them without having to define the model each time. For example, to use AlexNet, you can simply import the `models` module from `torchvision` and call `models.alexnet(num_classes=2)` to get the model definition. Definitions for other popular architectures such as VGG, ResNet, Inception, DenseNet, and SqueezeNet are also available.

In addition to getting the model definition, you can also download a pretrained set of weights for the model by calling `models.alexnet(pretrained=True)`. This allows you to use the model immediately for classification without any extra training. However, you may want to do some additional training on your specific dataset to improve accuracy.

While using the provided models is convenient, there is value in building the models yourself at least once to get a feel for how they fit together. This can help you practice building model architectures within PyTorch and understand how the different components work together. You can also compare your implementation with the provided models to make sure they match.

In summary, PyTorch provides many popular CNN architectures by default in the torchvision library, making it easy to use them in your applications. You can also download pretrained weights for these models to use them immediately for classification tasks.

### Examining a Model’s Structure

If you're curious about how a model is constructed, PyTorch provides an easy way to examine its structure. For example, to see the entire ResNet-18 architecture, you can simply call `print(model)`.

### Which Model Should You Use?

When it comes to choosing which model to use, the answer is whichever one works best for your specific application. While NASNet and PNAS architectures have achieved impressive results on ImageNet, they can be memory-hungry in operation and transfer learning may not be as effective as with other architectures such as ResNet.

One way to determine which model to use is to look at the winning entries in image-based competitions on Kaggle, a website that runs data science competitions. Many winning entries use ResNet-based ensembles. The ResNet architecture is a popular choice because it offers good accuracy and it's easy to start experimenting with smaller ResNets and then move to larger ones once you have something promising.

In summary, there are many powerful CNN architectures available and the best one for your application will depend on your specific needs and requirements. Examining the structure of different models and looking at their performance in competitions can help you make an informed decision.

## One-Stop Shopping for Models: PyTorch Hub

PyTorch Hub is a recent addition to the PyTorch ecosystem that provides a central location for obtaining published models. It aims to make it easy to access models for various types of data, including images, text, audio, video, and more. To obtain a model from PyTorch Hub, you can use the `torch.hub` module and call `torch.hub.load()` with the appropriate parameters. For example, to load a pretrained ResNet-50 model, you can use the following code:

```python
model = torch.hub.load('pytorch/vision', 'resnet50', pretrained=True)
```

The first parameter specifies the GitHub owner and repository where the model is located, while the second parameter specifies the model requested. The third parameter indicates whether to download pretrained weights for the model.

You can also use `torch.hub.list()` to discover all the models available in a given repository. For example, to see all the models available in the `pytorch/vision` repository, you can use the following code:

```python
models = torch.hub.list('pytorch/vision')
```

PyTorch Hub is still relatively new, so there may not be a huge number of models available yet. However, it is expected to become a popular way to distribute and download models in the future. All the models discussed in this chapter can be loaded through the `pytorch/vision` repository in PyTorch Hub.

## Conclusion

In this chapter, you have learned about how CNN-based neural networks work, including features such as Dropout, MaxPool, and BatchNorm. You have also looked at some of the most popular architectures used in the industry today. Before moving on to the next chapter, you can experiment with these architectures and see how they compare. Remember, you don't need to train them from scratch - you can simply download the pretrained weights and test the model.

In the next chapter, you will learn how to use these pretrained models as a starting point for a custom solution to the cats versus fish problem using transfer learning. This will allow you to leverage the power of these architectures to achieve impressive results on your specific task. 😊
