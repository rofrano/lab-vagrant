# Vagrant, VirtualBox, & Docker Lab

This lab will show you how to use Vagrant, VirtualBox, and Docker to automate the creations of development environments. As an example, it creates a Python / Flask / Redis development environment using Vagrant and VirtualBox to set up the Python development environment, and Docker to set up the Redis server.

By creating a ```Vagrantfile``` for all of your projects, you can provide developers with an "Instant Development Environment" the runs the same on their machine as every other machine eliminating the excuse _"It Works on My Machine!"_

## Instant Development Environment

This all each developer needs to do to get a consistent development environment to code, debug, and test with:

    git clone https://github.com/rofrano/lab-vagrant.git
    cd lab-vagrant
    vagrant up

## Additions to Vagrantfile

The following additions were made to the ```Vagrantfile``` to auto provision a complete development environment:

### Forward ports from vm to host

    config.vm.network "forwarded_port", guest: 5000, host: 5000

### Control the vm memory and cpus

    config.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 1
    end

### Set up development environment

    config.vm.provision "shell", inline: <<-SHELL
      sudo apt-get update
      sudo apt-get install -y git python-pip python-dev build-essential
      sudo apt-get -y autoremove
      # Install app dependencies
      cd /vagrant
      sudo pip install -r requirements.txt
      # Prepare Redis data share
      sudo mkdir -p /var/lib/redis/data
      sudo chown vagrant:vagrant /var/lib/redis/data
      # Make vi look nice
      echo "colorscheme desert" > ~/.vimrc
    SHELL

### Provision Docker containers for Redis

    config.vm.provision "docker" do |d|
      d.pull_images "redis:alpine"
      d.run "redis:alpine",
        args: "--restart=always -d --name redis -h redis -p 6379:6379 -v /var/lib/redis/data:/data"
    end

### Run the Application

Once you have used ```vagtant up``` to start the vm use:

    vagrant ssh
    cd /vagrant
    python app.py

You should now be able to test the application with the following URL:

[localhost:5000/hits](http://localhost:5000/hits)

Every time you access the URL the counter should increase by one.
