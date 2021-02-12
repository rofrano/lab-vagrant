# Vagrant, VirtualBox, & Docker Lab

This lab will show you how to use Vagrant, VirtualBox, and Docker to automate the creations of development environments. As an example, it creates a Python / Flask / Redis development environment using Vagrant and VirtualBox to set up the Python development environment, and Docker to set up the Redis server.

By creating a `Vagrantfile` for all of your projects, you can provide developers with an "Instant Development Environment" the runs the same on their machine as every other machine eliminating the excuse _"It Works on My Machine!"_

## Instant Development Environment

This all each developer needs to do to get a consistent development environment to code, debug, and test with:

```shell
    git clone https://github.com/rofrano/lab-vagrant.git
    cd lab-vagrant
    vagrant up
```

### Note: Apple M1 Chip Owners

If you are _lucky / unluckly_ enough to have a new 2020 Mac with the **Apple M1 chip** which is based on **ARM** architecture, you CANNOT use VirtualBox because VirtualBox requires an **Intel** architecture processor to run. The good news is that [Docker](https://www.docker.com) has introduced the [Apple M1 Tech Preview](https://docs.docker.com/docker-for-mac/apple-m1/) that runs Docker on Macs that have the Apple M1 chip. By using Docker as a provider for Vagrant, we can simulate the same experience as developers using Vagrant with VirtualBox.

To use **Docker** as your provider use:

```sh
vagrant up --provider=docker
```

This will use a Docker image that I have prepared for use with Vagrant. Unfortunately, you will get the following error:

```sh
Docker is not running on the guest VM.
```

I haven't figured out why this happens but it only happens when creating the container initially. To fix it, just run the following command:

```sh
vagrant provision
```

This will reprovision and pull down the Redis container and complete successfully.

## Additions to Vagrantfile

The following additions were made to the `Vagrantfile` to auto provision a complete development environment:

### Forward ports from vm to host

Our Python Flask apps listens on port `5000` by default so we need to forward the port from
inside the VM to our workstation so that we can access it with our browser.

```ruby
    config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
```

### Control the vm memory and cpus

Python Flask is very light weight and should only need a minimal VM.

```ruby
    config.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
      vb.cpus = 1
    end
```

### Set up development environment

Installing all of the dependencies with Vagrant ensures that everyone gets the same
environment configured exactly the same way every time.

```ruby
      config.vm.provision "shell", inline: <<-SHELL
        # Update and install
        apt-get update
        apt-get install -y git tree python3-dev python3-pip python3-venv apt-transport-https
        apt-get upgrade python3
        apt-get -y autoremove

        # Install app dependencies
        cd /vagrant
        pip3 install -r requirements.txt
      SHELL

```

### Provision Docker containers for Redis

**Vagrant** supports **Docker** natively so let's take advantage of that and
provision our **Redis** database using Docker.

```ruby
    config.vm.provision "docker" do |d|
      d.pull_images "redis:alpine"
      d.run "redis:alpine",
        args: "--restart=always -d --name redis -h redis -p 6379:6379 -v redis_data:/data"
    end
```

### Run the Application

Once you have used `vagrant up` to start the vm use:

```shell
    vagrant ssh
    cd /vagrant
    python app.py
```

You should now be able to test the application with the following URL:

[localhost:5000/hits](http://localhost:5000/hits)

Every time you access the URL the counter should increase by one.
