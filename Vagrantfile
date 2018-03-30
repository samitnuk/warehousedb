# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :vagrant_vm do |vm_config|
    vm_config.vm.box = "ubuntu/xenial64"  # Ubuntu 16.04
    vm_config.vm.network :private_network, ip: "10.0.0.10"
    vm_config.vm.network :forwarded_port, guest: 80, host: 8080

    vm_config.vm.provision :shell, path: "ansible/vagrant/vagrant_initial.sh", privileged: false

    vm_config.vm.provision "shell" do |s|
      ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
      s.inline = <<-SHELL
        echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
        echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
      SHELL
    end

  end

end
