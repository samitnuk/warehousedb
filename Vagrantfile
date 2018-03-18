# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define :vagrant_vm do |vm_config|
    vm_config.vm.box = "ubuntu/xenial64"  # Ubuntu 16.04
    vm_config.vm.network :private_network, ip: "10.0.0.10"
    vm_config.vm.network :forwarded_port, guest: 80, host: 8080

    vm_config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/vagrant/python36.yaml"
      ansible.extra_vars = {
        # Sinse Ubuntu 16.04 does not have "/usr/bin/python" (python 2 is not installed)
        ansible_python_interpreter: "/usr/bin/python3.5",
      }
    end

  end

end
