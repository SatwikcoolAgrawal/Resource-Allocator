# Resource Allocation System

This Python program simulates a simple resource allocation system for managing physical hosts and virtual machines (VMs). It includes functionalities to add/delete hosts and VMs, allocate VMs to hosts based on resource availability, and view the current allocation status.

## Features

- Add physical hosts with specified CPU and memory capacity.
- Add VMs with specific CPU and memory requirements.
- Allocate VMs to the most suitable hosts based on a load-balancing algorithm.
- Delete VMs and hosts.
- View current allocation status of VMs to hosts.
- Redistribute VMs when a new host is added to ensure load balancing.

## Usage

### Running the Program

Run the `main()` function in the Python script. It provides a menu-based interface to interact with the resource allocation system.

### Menu Options

1. **Add a host**: Add a new physical host by providing an ID, total CPU, and total memory.
2. **Add a VM**: Add a new VM by providing an ID, required CPU, and required memory.
3. **View hosts**: View details of all the hosts, including their used and total resources, and allocated VMs.
4. **View VMs**: View details of all the VMs, including their CPU, memory, and the host they are allocated to (if any).
5. **Allocate VM to best host**: Allocate a VM to the most suitable host based on the load-balancing algorithm.
6. **Delete a VM**: Delete a specified VM by its ID.
7. **Delete a host**: Delete a specified host by its ID. Any VMs allocated to this host will be reallocated to other hosts.
8. **View current allocation status**: View the current allocation of VMs to hosts.
9. **Exit**: Exit the program.

## Allocation Algorithm

The allocation algorithm aims to distribute VMs across hosts to achieve load balancing. Here’s how it works:

### Steps

1. **Calculate Load Factor**:
    - For each host, compute the load factor if the VM were to be allocated to it.
    - The load factor is calculated as:
    $$\text{loadFactor} = \left( \frac{\text{remainingCpu}}{\text{totalCpu}} \right) + \left( \frac{\text{remainingMemory}}{\text{totalMemory}} \right) - \left( \frac{\text{numberOfVms}}{\text{avgVmsPerHost} + 1} \right)$$
      Where:
      - `remaining_cpu` = `host.total_cpu` - `host.used_cpu` - `vm.cpu`
      - `remaining_memory` = `host.total_memory` - `host.used_memory` - `vm.memory`
      - `number_of_vms` = Number of VMs in the host + 1 (including the new VM)
      - `avg_vms_per_host` = Average number of VMs per host across all hosts

2. **Select Best Host**:
    - Iterate through all hosts to find the one that can allocate the VM and has the highest load factor.
    - If a suitable host is found, allocate the VM to this host.

3. **Redistribute VMs**:
    - When a new host is added, all VMs are temporarily removed from their current hosts.
    - Each VM is then reallocated to ensure even distribution across all available hosts.
