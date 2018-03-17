# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :production do |production_config|
    production_config.vm.box = "ubuntu/xenial64"
    production_config.vm.network :forwarded_port, guest: 80, host: 8080, host_ip: "127.0.0.1"
    production_config.vm.network :private_network, ip: "42.42.42.42"
  end

end
