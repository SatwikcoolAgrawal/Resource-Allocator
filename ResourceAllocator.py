import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

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
        vm_list = list(host.vms)
        del self.hosts[host_id]
        for vm in vm_list:
            self.allocate_vm(vm.id)

class ResourceAllocationApp:
    def __init__(self, root):
        self.system = ResourceAllocationSystem()

        ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        root.title("Resource Allocation System")
        root.geometry("600x400")

        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.label = ctk.CTkLabel(self.main_frame, text="Resource Allocation System", font=("Arial", 16))
        self.label.pack(pady=10)

        self.menu_frame = ctk.CTkFrame(self.main_frame)
        self.menu_frame.pack(pady=10)

        self.add_host_button = ctk.CTkButton(self.menu_frame, text="Add a Host", command=self.add_host)
        self.add_host_button.grid(row=0, column=0, padx=5, pady=5)

        self.add_vm_button = ctk.CTkButton(self.menu_frame, text="Add a VM", command=self.add_vm)
        self.add_vm_button.grid(row=0, column=1, padx=5, pady=5)

        self.view_hosts_button = ctk.CTkButton(self.menu_frame, text="View Hosts", command=self.view_hosts)
        self.view_hosts_button.grid(row=1, column=0, padx=5, pady=5)

        self.view_vms_button = ctk.CTkButton(self.menu_frame, text="View VMs", command=self.view_vms)
        self.view_vms_button.grid(row=1, column=1, padx=5, pady=5)

        self.allocate_vm_button = ctk.CTkButton(self.menu_frame, text="Allocate VM to Best Host", command=self.allocate_vm)
        self.allocate_vm_button.grid(row=2, column=0, padx=5, pady=5)

        self.delete_vm_button = ctk.CTkButton(self.menu_frame, text="Delete a VM", command=self.delete_vm)
        self.delete_vm_button.grid(row=2, column=1, padx=5, pady=5)

        self.delete_host_button = ctk.CTkButton(self.menu_frame, text="Delete a Host", command=self.delete_host)
        self.delete_host_button.grid(row=3, column=0, padx=5, pady=5)

        self.view_allocation_button = ctk.CTkButton(self.menu_frame, text="View Allocation Status", command=self.view_allocation_status)
        self.view_allocation_button.grid(row=3, column=1, padx=5, pady=5)

        self.exit_button = ctk.CTkButton(self.menu_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.output_frame = ctk.CTkFrame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = ctk.CTkTextbox(self.output_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def add_host(self):
        self.input_dialog("Add a Host", self.add_host_action)

    def add_vm(self):
        self.input_dialog("Add a VM", self.add_vm_action)

    def view_hosts(self):
        self.display_output(self.system.view_hosts())

    def view_vms(self):
        self.display_output(self.system.view_vms())

    def allocate_vm(self):
        self.input_dialog("Allocate VM to Best Host", self.allocate_vm_action, is_vm=True)

    def delete_vm(self):
        self.input_dialog("Delete a VM", self.delete_vm_action, is_vm=True)

    def delete_host(self):
        self.input_dialog("Delete a Host", self.delete_host_action)

    def view_allocation_status(self):
        self.display_output(self.system.view_allocation_status())

    def input_dialog(self, title, action, is_vm=False):
        dialog = ctk.CTkToplevel()
        dialog.title(title)
        dialog.geometry("300x200")

        id_label = ctk.CTkLabel(dialog, text="Enter ID:")
        id_label.pack(pady=5)
        id_entry = ctk.CTkEntry(dialog)
        id_entry.pack(pady=5)

        if not is_vm:
            cpu_label = ctk.CTkLabel(dialog, text="Enter Total CPU:")
            cpu_label.pack(pady=5)
            cpu_entry = ctk.CTkEntry(dialog)
            cpu_entry.pack(pady=5)

            memory_label = ctk.CTkLabel(dialog, text="Enter Total Memory:")
            memory_label.pack(pady=5)
            memory_entry = ctk.CTkEntry(dialog)
            memory_entry.pack(pady=5)
        else:
            cpu_label = ctk.CTkLabel(dialog, text="Enter Required CPU:")
            cpu_label.pack(pady=5)
            cpu_entry = ctk.CTkEntry(dialog)
            cpu_entry.pack(pady=5)

            memory_label = ctk.CTkLabel(dialog, text="Enter Required Memory:")
            memory_label.pack(pady=5)
            memory_entry = ctk.CTkEntry(dialog)
            memory_entry.pack(pady=5)

        def submit_action():
            try:
                if not is_vm:
                    action(id_entry.get(), int(cpu_entry.get()), int(memory_entry.get()))
                else:
                    action(id_entry.get(), int(cpu_entry.get()), int(memory_entry.get()))
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")

        submit_button = ctk.CTkButton(dialog, text="Submit", command=submit_action)
        submit_button.pack(pady=10)

    def add_host_action(self, id, total_cpu, total_memory):
        try:
            self.system.add_host(id, total_cpu, total_memory)
            self.display_output(f"Host {id} added.")
        except InsufficientResourcesException as e:
            self.display_output(str(e))
        except Exception as e:
            self.display_output("Error occurred.")

    def add_vm_action(self, id, cpu, memory):
        try:
            self.system.add_vm(id, cpu, memory)
            self.display_output(f"VM {id} added.")
        except Exception as e:
            self.display_output("Error occurred.")

    def allocate_vm_action(self, vm_id, cpu, memory):
        try:
            self.system.allocate_vm(vm_id)
            self.display_output(f"VM {vm_id} allocated to the best host.")
        except (InsufficientResourcesException, ResourceNotFoundException) as e:
            self.display_output(str(e))

    def delete_vm_action(self, vm_id):
        try:
            self.system.delete_vm(vm_id)
            self.display_output(f"VM {vm_id} deleted.")
        except ResourceNotFoundException as e:
            self.display_output(str(e))

    def delete_host_action(self, host_id):
        try:
            self.system.delete_host(host_id)
            self.display_output(f"Host {host_id} deleted.")
        except ResourceNotFoundException as e:
            self.display_output(str(e))

    def display_output(self, message):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, message)
        self.output_text.configure(state=tk.DISABLED)

if __name__ == "__main__":
    root = ctk.CTk()
    app = ResourceAllocationApp(root)
    root.mainloop()
