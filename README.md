# Resource-Allocator
System where you are given a list of virtual machines, each with its requested CPU and memory resources, and a list of physical hosts with available CPU and memory resources. The System handles the resource allocation, i.e, to assign virtual machines to physical hosts in a way that maximises resource utilisation and maintains fairness.

Allocation Algorithm
The allocation algorithm aims to efficiently allocate virtual machines (VMs) to physical hosts while ensuring balanced resource utilization. The main steps are as follows:

Steps
Adding a Physical Host:

When a new physical host is added, it's appended to the list of hosts.
The list of hosts is then sorted to ensure that the most suitable host for future VM allocations is at the top.
Adding a Virtual Machine:

When a new VM is added, it's appended to the list of VMs.
The algorithm attempts to allocate the VM to the best available host.
The list of hosts is sorted again to ensure balanced allocation.
Allocating a VM to a Host:

The allocation process involves iterating through the list of physical hosts.
For each host, the algorithm checks if it has enough available resources (RAM and memory) to accommodate the VM.
If a suitable host is found, the VM is allocated to this host, and the available resources of the host are updated.
The list of hosts is then sorted to maintain a balanced allocation.
Deallocating a VM:

When a VM is removed, it is deallocated from its current host, and the available resources of the host are updated.
The list of hosts is sorted again to maintain balance.
Removing a Host:

When a host is removed, all VMs currently allocated to this host are reallocated to other hosts.
The list of hosts is sorted again to maintain balance.
Sorting Hosts
The sorting of hosts is based on two criteria:

Number of VMs: Hosts with fewer VMs are preferred.
Resource Utilization: Among hosts with the same number of VMs, those with more available resources (RAM and memory) are preferred.
