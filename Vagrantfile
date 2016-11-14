# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    #vb.gui = true
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 1
  end

  # Copy your .gitconfig file so that your credentials are correct
  # config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.

  ######################################################################
  # Add Python Flask environment
  ######################################################################
  # Forward Python Flask port
  config.vm.network :forwarded_port, guest: 5000, host: 5000, auto_correct: true

  # Setup a Python development environment
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y git python-pip python-dev build-essential
    sudo apt-get -y autoremove
    # Install app dependencies
    cd /vagrant
    sudo pip install -r requirements.txt
  SHELL

  ######################################################################
  # Add Redis docker container
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Prepare Redis data share
    sudo mkdir -p /var/lib/redis/data
    sudo chown vagrant:vagrant /var/lib/redis/data
  SHELL

  # Add Redis docker container
  config.vm.provision "docker" do |d|
    d.pull_images "redis:alpine"
    d.run "redis:alpine",
      args: "--restart=always -d --name redis -h redis -p 6379:6379 -v /var/lib/redis/data:/data"
  end

end
