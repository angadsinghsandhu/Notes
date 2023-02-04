# Docker WorkFlow

To work with Docker we take an application and `"dockerize it"` which means we make a small change so that it can be run by docker i.e we add a `Dockerfile` to it. A docker file is a plain text file that includes instructions that docker uses to package up this application into an `Docker Image`. This image contains everything our application needs to run.

An Image may typically contain:

- a cut down operating system
- a runtime environment (like node or python)
- application files
- third-party libraries
- environment variables

Hence, we create a docker file and give it to docker for packaging our application into an image once we have an image, docker can start a container using that image. A container is just a process but it's a special kind of process because it has its own file system which is provided by the image.

Our application gets loaded inside a container or a process and this is how we run our application locally on our development machine, instead of directly launching the application and running it inside a typical process we tell docker to run it inside a container an isolated environment.

the beauty of docker is that, once we have this image we can push it to a `Docker Registry` like `Docker HUB` (docker hub/docker is analogous to like github/git, it's a storage for docker images that anyone can use). Once the application image is on docker hub then we can put it on any machines running docker and run it independently in that machine.

we no longer need to maintain long and complex `release documents` that have to be precisely followed. All the
**instructions for building** an image of an application are written in a Dockerfile with that we can package up our application into an image and run it virtually anywhere.

## Example: Docker Workflow in Action

The application is inside the `\example\hello-docker` directory withing this folder, Here is the step-by-step guide on how to biuld and publish this with docker:

1. Create a new `\hello-docker` directory
2. open that directory in your IDE
3. Create a smaple JavaScript page (Treat this as our application)
4. Dockerize this app (packaging the app and adding all launch instructions)
5. Add `Dockerfile` to the project
6. Add appropriate launch info. More info [HERE](https://thenewstack.io/docker-basics-how-to-use-dockerfiles/)
7. run `docker build -t hello-docker .` to create the image. More info [HERE](https://devopscube.com/build-docker-image/)
8. run `docker image ls`to get all the docker images on a system.
9. run `docker run hello-docker` to start the image.
10. publish the image on `docker hub` by running `docker push hello-docker`.

If we did not use docker we would have to perform these steps on our deployment machine to run this application:

1. start with OS
2. Install Node
3. Copy app files
4. run `node app.js`

Now with Docker we can simply do omething like:

1. run `docker pull angadsandhuwork/hello-docker` on a machine with Docker installed.
2. execute `docker run angadsandhuwork/hello-docker` to run the image.
