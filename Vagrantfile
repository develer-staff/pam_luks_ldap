SECONDARY_VDI = File.join(File.dirname(File.expand_path(__FILE__)), "sdb.vdi")

Vagrant.configure(2) do |config|
    config.vm.box = "boxcutter/ubuntu1404"

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provision/provision.yml"
    end

    config.vm.provider "virtualbox" do |v|
        unless File.exists?(SECONDARY_VDI)
            v.customize ["createhd", "--filename", SECONDARY_VDI, "--size", 1024]
        end

        v.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 1, "--device", 0, "--type", "hdd", "--medium", SECONDARY_VDI]
    end
end
