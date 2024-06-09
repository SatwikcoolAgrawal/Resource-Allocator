class InsufficientResourcesException(Exception):
    pass

class ResourceNotFoundException(Exception):
    pass

class Host:
    def __init__(self, id, total_cpu, total_memory):
        self.id = id
        self.total_cpu = total_cpu
        self.total_memory = total_memory
        self.used_cpu = 0
        self.used_memory = 0
        self.vms = []

    def add_vm(self, vm):
        if self.can_allocate(vm):
            self.vms.append(vm)
            self.used_cpu += vm.cpu
            self.used_memory += vm.memory
            vm.host = self
        else:
            raise InsufficientResourcesException("Insufficient resources on the host")

    def can_allocate(self, vm):
        return self.total_cpu - self.used_cpu >= vm.cpu and self.total_memory - self.used_memory >= vm.memory

    def remove_vm(self, vm):
        if vm in self.vms:
            self.vms.remove(vm)
            self.used_cpu -= vm.cpu
            self.used_memory -= vm.memory
            vm.host = None


class VM:
    def __init__(self, id, cpu, memory):
        self.id = id
        self.cpu = cpu
        self.memory = memory
        self.host = None


class ResourceAllocationSystem:
    def __init__(self):
        self.hosts = {}
        self.vms = {}

    def add_host(self, id, total_cpu, total_memory):
        self.hosts[id] = Host(id, total_cpu, total_memory)
        self.redistribute_vms()

    def add_vm(self, id, cpu, memory):
        self.vms[id] = VM(id, cpu, memory)

    def allocate_vm(self, vm_id):
        vm = self.vms.get(vm_id)
        if not vm:
            raise ResourceNotFoundException("VM not found")

        best_host = None
        max_load_factor = float('-inf')

        for host in self.hosts.values():
            if host.can_allocate(vm):
                load_factor = self.calculate_load_factor(vm, host)
                if load_factor > max_load_factor:
                    best_host = host
                    max_load_factor = load_factor

        if best_host:
            if vm.host:
                vm.host.remove_vm(vm)
            best_host.add_vm(vm)
        else:
            raise InsufficientResourcesException("No suitable host found for the VM")

    def calculate_load_factor(self, vm, host):
        remaining_cpu = host.total_cpu - host.used_cpu - vm.cpu
        remaining_memory = host.total_memory - host.used_memory - vm.memory
        number_of_vms = len(host.vms) + 1

        avg_vms_per_host = sum(len(h.vms) for h in self.hosts.values()) / len(self.hosts)
        cpu_utilization = (remaining_cpu / host.total_cpu)
        memory_utilization = (remaining_memory / host.total_memory)
        vm_balance = (number_of_vms / (avg_vms_per_host + 1))

        load_factor = cpu_utilization + memory_utilization - vm_balance
        return load_factor

    def redistribute_vms(self):
        all_vms = list(self.vms.values())
        for vm in all_vms:
            if vm.host:
                vm.host.remove_vm(vm)
        for vm in all_vms:
            self.allocate_vm(vm.id)

    def view_hosts(self):
        return [
            {
                'id': host.id,
                'total_cpu': host.total_cpu,
                'used_cpu': host.used_cpu,
                'total_memory': host.total_memory,
                'used_memory': host.used_memory,
                'vms': [vm.id for vm in host.vms]
            }
            for host in self.hosts.values()
        ]

    def view_vms(self):
        return [
            {
                'id': vm.id,
                'cpu': vm.cpu,
                'memory': vm.memory,
                'host_id': vm.host.id if vm.host else None
            }
            for vm in self.vms.values()
        ]

    def view_allocation_status(self):
        allocation_status = {}
        for host in self.hosts.values():
            allocation_status[host.id] = [vm.id for vm in host.vms]
        return allocation_status

    def delete_vm(self, vm_id):
        vm = self.vms.get(vm_id)
        if not vm:
            raise ResourceNotFoundException("VM not found")
        if vm.host:
            vm.host.remove_vm(vm)
        del self.vms[vm_id]

    def delete_host(self, host_id):
        host = self.hosts.get(host_id)
        if not host:
            raise ResourceNotFoundException("Host not found")
        vm_list=list(host.vms)
        del self.hosts[host_id]
        for vm in vm_list:
            self.allocate_vm(vm.id)


def main():
    system = ResourceAllocationSystem()

    while True:
        print("\nResource Allocation System")
        print("1. Add a host")
        print("2. Add a VM")
        print("3. View hosts")
        print("4. View VMs")
        print("5. Allocate VM to best host")
        print("6. Delete a VM")
        print("7. Delete a host")
        print("8. View current allocation status")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            id = input("Enter host ID: ")
            total_cpu = int(input("Enter total CPU: "))
            total_memory = int(input("Enter total memory: "))
            system.add_host(id, total_cpu, total_memory)
            print(f"Host {id} added.")
        elif choice == '2':
            id = input("Enter VM ID: ")
            cpu = int(input("Enter required CPU: "))
            memory = int(input("Enter required memory: "))
            system.add_vm(id, cpu, memory)
            print(f"VM {id} added.")
        elif choice == '3':
            hosts = system.view_hosts()
            for host in hosts:
                print(host)
        elif choice == '4':
            vms = system.view_vms()
            for vm in vms:
                print(vm)
        elif choice == '5':
            vm_id = input("Enter VM ID to allocate: ")
            try:
                system.allocate_vm(vm_id)
                print(f"VM {vm_id} allocated to the best host.")
            except (InsufficientResourcesException, ResourceNotFoundException) as e:
                print(e)
        elif choice == '6':
            vm_id = input("Enter VM ID to delete: ")
            try:
                system.delete_vm(vm_id)
                print(f"VM {vm_id} deleted.")
            except ResourceNotFoundException as e:
                print(e)
        elif choice == '7':
            host_id = input("Enter host ID to delete: ")
            try:
                system.delete_host(host_id)
                print(f"Host {host_id} deleted.")
            except ResourceNotFoundException as e:
                print(e)
        elif choice == '8':
            allocation_status = system.view_allocation_status()
            for host_id, vm_ids in allocation_status.items():
                print(f"Host {host_id}: VMs {vm_ids}")
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()