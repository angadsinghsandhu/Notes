# Docker Architecture

docker uses a `client-server` architecture so it has a client component that talks to a server component (aka `docker engine`) using a restful api the server. Docker Engine sits in the background and takes care of building and running docker containers.

Technically a container is just a `process` like other processes running on your computer but it's a special kind of process. Unlike virtual machines containers don't contain a full-blown OS instead all containers on a host share the OS of the host. More accurately all containers share the `kernel` of the host.

A kernel is the **core of an operating system** (like the engine of a car). It's the part that manages all applications as well as hardware resources like memory and cpu. Every OS has its own kernel or engine and these kernels have different apis that's why we cannot run a windows application on linux because under the hood this application needs to talk to the kernel of the underlying OS.

Hence, a linux machine we can only run linux containers because these containers need linux on a windows machine however we can run both windows and linux containers because windows 10 is now shipped with a custom built linux kernel (in addition to the windows kernel already there) 

So with this linux kernel now we can run linux applications natively on windows. Thus, windows can run both linux and windows containers. The windows containers share the windows kernel and the linux containers share the linux kernel.

Mac OS has its own kernel which is different from linux and windows kernels and this kernel does not have native support for continuous applications so docker on mac uses a lightweight linux virtual machine.

## Docker Installation

- [Docker Installation Guide](https://docs.docker.com/engine/install/)
- [Docker Installation on Windows](https://www.youtube.com/watch?v=5nX8U8Fz5S0)
- [Docker Installation on Linux](https://www.youtube.com/watch?v=TDLKQWsrSyk)
- [Docker Installation on Mac OS](https://www.youtube.com/watch?v=SGmFGYCuJK4)
