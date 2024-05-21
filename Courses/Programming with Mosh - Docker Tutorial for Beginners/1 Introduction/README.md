# Introduction to docker

## In this section

- What is docker
- Virtual Machineas vs Containers
- Architecture of Docker
- Installing Docker
- Development Workflow

## What is Docker?

*It is an application for building, running and shipping applications In a consistant manner so that ones' application runs the same way on different machines.*

Docker arises form issues in shipping code, where an application running perfectly on one machine might not run on another machine. some of the reasons this might happe are:

- Missing Files
- Software Version Mismatch
- Different config setting (env variables)

With docker we can package an application and run it anywhere, and time wastage on setting up machines and dependencies can be minimized. With docker 2 applications with different dependencies can run simultaneously without problems. Each application runs with its dependcies in an isolated env.

## Virtual Machines vs Containers

| CONTAINER                        | VIRTUAL MACHINE (VM)             |
| -------------------------------- | -------------------------------- |
| An Isolated enviornment to run an application | An abstraction of a machine |
| This is created using apps like Docker that runinside a VM | This is implemented by a Hypervisor on a mahine that lets one run multiple OS/VM |
| Easy to use, Fast, Resouce Light | COmplicated, Slow, Resource Heavy |
| Example: Docker, Podman, LXD | Example: VirtualBox, VMware, Hyper-v |
