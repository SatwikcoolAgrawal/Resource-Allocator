import functools

class VirtualMachine:
    CurrId=1
    def __init__(self, inputRam:int=0, inputMemory:int=0):
        self.id:int = VirtualMachine.CurrId
        VirtualMachine.CurrId+=1
        self.ram:int = inputRam
        self.memory:int = inputMemory
        self.host=None

    def printDetail(self)->None:
        print(f"Virtual Machine {self.id}")
        print(f"Ram required :{self.ram}")
        print(f"Memory required :{self.memory}\n")

    def allocateHost(self,host)->None:
        self.host=host

    def deallocate(self)->None:
        self.host=None


class PhysicalHost:
    
    CurrId:int= 1
    
    def __init__(self , inputRam:int=0, inputMemory:int=0)->None:
        self.id:int =PhysicalHost.CurrId
        PhysicalHost.CurrId+=1 
        self.totalRam:int = inputRam
        self.totalMemory:int = inputMemory
        self.availableRam:int = inputRam
        self.availableMemory:int = inputMemory
        self.Vms:list = []

    def printDetail(self)->None:
        print(f"Physical Host {self.id}")
        print(f"Total Ram :{self.totalRam} && Available Ram :{self.availableRam}")
        print(f"Total Memory :{self.totalMemory} && Available Memory :{self.availableMemory}")
        print(f"List of Allocated Vm:")
        for v in  self.Vms:
            v.printDetail()
        print()

    def isPossibleToAllocate(self, vm:VirtualMachine)->bool:
        return vm.memory <= self.availableMemory and vm.ram <= self.availableRam

    def AllocateVm(self, vm:VirtualMachine)->bool:
        if self.isPossibleToAllocate(vm):
            self.Vms.append(vm)
            vm.allocateHost(self)
            self.availableMemory -= vm.memory
            self.availableRam -= vm.ram
            return True
        else:
            return False

    def DeallocateVm(self, vm:VirtualMachine)->None:
        self.Vms.remove(vm)
        self.availableMemory+=vm.memory
        self.availableRam+=vm.ram

class ResourceAllocator:
    
    def __init__(self):
        self.VirtualMachines:list=[]
        self.PhysicalHosts:list=[]

    
    # def compare(self,a, b)->bool:
    #     if len(a.Vms) != len(b.Vms): # Compare by the number of Vms
    #         return len(a.Vms) < len(b.Vms)
    #     return a.availableMemory * a.availableRam > b.availableMemory * b.availableRam
    
    
    def sortHost(self):
        self.PhysicalHosts.sort(key=lambda x: (-1*len(x.Vms),x.availableMemory*x.availableRam),reverse=True)



    def addHost(self,ram,memo):
        newHost=PhysicalHost(ram,memo)
        self.PhysicalHosts.append(newHost)
        self.sortHost()
        return newHost


    def addVm(self,ram,memo):
        newVm=VirtualMachine(ram,memo)
        self.VirtualMachines.append(newVm)
        self.allocateHostToVm(newVm)
        return newVm
    
    def allocateHostToVm(self,newVm:VirtualMachine):
        for h in self.PhysicalHosts:
            if h.AllocateVm(newVm):
                self.sortHost()
                print(f'VM{newVm.id} is allocated to PhyHost{h.id}\n')
                return True
        
        print(f"Can't Allocate Vm{newVm.id} to Any Host\n")
        return False
    
    def RemoveHost(self,host:PhysicalHost):
        self.PhysicalHosts.remove(host)
        for vm in host.Vms:
            self.allocateHostToVm(vm)
    
    def removeVm(self,vm:VirtualMachine):
        self.VirtualMachines.remove(vm)
        vm.host.DeallocateVm(vm)
        self.sortHost()
        vm.deallocate()

    def printDetail(self):
        for ph in self.PhysicalHosts:
            ph.printDetail()



if __name__=="__main__":
    allocator=ResourceAllocator()
    Ps={}
    Vs={}
    while (True):
        print("""
              1: Add New Physical Host
              2: Add New Virtual Machine
              3: Remove Host
              4: Remove VM
              else: Exit
              """)
        task=int(input("Enter Your Task :"))

        match task:
            case 1:
                myram=int(input("Enter Host's Ram: "))
                mymemo=int(input("Enter Host's Memory: "))
                x=allocator.addHost(myram,mymemo)
                print("-------------------------------------")
                Ps[x.id]=x
                allocator.printDetail()
            case 2:
                myram=int(input("Enter Vm's Ram: "))
                mymemo=int(input("Enter Vm's Memory: "))
                y=allocator.addVm(myram,mymemo)
                print("-------------------------------------")
                Vs[y.id]=y
                allocator.printDetail()
            case 3:
                hostid=int(input("Enter Host Id :"))
                allocator.RemoveHost(Ps[hostid])
                print("-------------------------------------")
                allocator.printDetail()
            case 4:
                Vmid=int(input("Enter VM Id :"))
                allocator.removeVm(Vs[Vmid])
                print("-------------------------------------")
                allocator.printDetail()
            case default:
                break