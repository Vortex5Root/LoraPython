from threading import Thread
import serial
import serial.tools.list_ports
'''
ola = list(serial.tools.list_ports.comports(include_links=False))
for i in ola:
    print('-----------------------')
    print('Index:',ola.index(i))
    print('   Product:',i.product)
    print('   Device:',i.device)
    print('-----------------------')
porte = ''
while True:
    try:
        porte = ola[int(input('select the Index>'))].device
        break
    except:
        print('Invalid index')
ser = serial.Serial(port=porte,baudrate=9600)
print(ser.name)
while True:
    command = input('>')
    command += '\r\n'
    try:
        ser.write(command.encode())
        while True:
            try:
                print(ser.readline().decode())
            except:
                break
    except Exception as e:
        print(e)
'''#'''
def check_hex_from(string):
    for i in string:
        if i not in "0123456789ABCDEF":
            raise f"Invalid need To bee only Hex"
    return True

class LoRa_E5():

    def __init__(self):
        self.all_serials = list(serial.tools.list_ports.comports(include_links=False))

        self.tag = 'AT'

        self.errors = {
            "-1" : "Parameters is invalid",
            "-10" : "Command unknown",
            "-11" : "Command is in wrong format",
            "-12" : "Command is unavailable in current mode (Check with AT+MODE)",
            "-20" : "Too many parameters. LoRaWAN modem support max 15 parameters",
            "-21" : "Length of command is too long (exceed 528 bytes)",
            "-22" : "Receive end symbol timeout, command must end with <LF>",
            "-23" : "Invalid character received",
            "-24" : "Either -21, -22 or -23",
        }
        self.out_put = []
        self.get = True

    def select(self):
        for i in self.all_serials:
            print('-----------------------')
            print('Index:',self.all_serials.index(i))
            print('   Product:',i.product)
            print('   Device:',i.device)
            print('-----------------------')
        while True:
            try:
                idx = input('select the Index>')
                if idx.lower() == "exit":
                    break
                self.port = self.all_serials[int(idx)].device
                break
            except:
                print('Invalid index')

    def connect(self):
        self.conn = serial.Serial(port=self.port,baudrate=9600)

        return self.conn.name

    def get_return(self):
        while self.get:
            line = self.conn.readline()
            #print(line)
            try:
                error = line.decode().replace(')','').split('ERROR(')[1]
                #print(error)
                return self.get_error(error.replace('\r\n',''))
            except Exception as e:
                #print(e)
                return line
                break

    def get_out(self):
        return self.get_return()

    def get_error(self,error_code):
        return print(self.errors[error_code])

    '''
    -------------------------------------------
    |           Start of intraction           |
    -------------------------------------------
    '''

    def teste(self):
        temp_tag = self.tag+'\r\n'
        print(temp_tag.encode())
        #return None
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def version(self):
        temp_tag = self.tag+"+VER"+'\r\n'
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def identifier(self,id_type="",set_to=""):
        types_id = ["DevAddr","DevEui","AppEui"]
        error = [4,8,8]
        temp_tag = self.tag+"+ID"
        if id_type != "":
            if id_types in types_id:
                temp_tag += f"={id_type}"
                if set_to != "":
                    if len(set_to) != error[types_id.index(id_types)]:
                        raise f"Invalid Length need to have {error[types_id.index(id_types)]}"
                    check_hex_from(set_to)
                    temp_tag += f', "{set_to}"'
                self.conn.write(temp_tag.encode())
                return self.get_out()
            else:
                raise f"Invalid type {types_id}"
        else:
            self.conn.write(temp_tag.encode())
            out_put = []
            for i in range(5):
                out_put.append(self.get_out())
            out_put.pop(0)
            out_put.pop(0)
            return out_put

    def send_msg(self,message):
        temp_tag = self.tag+f'+MSG="{message}"'
        self.conn.write(temp_tag.encode())
        out_put = []
        for i in range(4):
            try:
                i = self.get_out()
                if i not in [b'+INFO: Input timeout\r\n',b'\r\n']:
                    out_put.append(i)
            except:
                return out_put
        return out_put

    def send_cmsg(self,message):
        temp_tag = self.tag+f'+CMSG="{message}"'
        self.conn.write(temp_tag.encode())
        out_put = []
        for i in range(5):
            info = self.get_out()
            print(info)
            out_put.append(info)
        out_put.pop(0)
        out_put.pop(0)
        return out_put

    def send_pmsg(self,message):
        temp_tag = self.tag+f'+PMSG="{message}"'
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def send_pmsghex(self,message):
        check_hex_from(msg_hex)
        temp_tag = self.tag+f'+PMSGHEX="{message}"'
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def set_conn(self,port):
        temp_tag = self.tag+f'+PORT="{message}"'
        if port == "?":
            self.conn.write(temp_tag.encode())
            return self.get_out()
        if port not in range(255):
            raise "The range to the ports is 0-255"
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def adr(self,mode):
        temp_tag = self.tag+f'+ADR'

        if mode.upper() == "ON" or mode.upper() == "OFF":
            temp_tag += "="+mode.upper()
            self.conn.write(temp_tag.encode())
            return self.get_out()
        raise "Mode ON/OFF !!"

    def set_data_rate(self,mode):
        temp_tag = self.tag+"+DR="
        if mode in ["drx","band","SCHEME"]:
            temp_tag += mode
            self.conn.write(temp_tag.encode())
            return self.get_out()
        raise "Only avalable drx,band, SHEME"

    def channels(self,query):
        temp_tag = self.tag+f"+CH={query}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def set_prower(self,power=None):
        if power == None:
            temp_tag = self.tag+f"+POWER"
        else:
            temp_tag = self.tag+f"+POWER={power}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def rept(self,rept_times):
        if retry_times in range(1,15):
            temp_tag = self.tag+f"+REPT={rept_times}"
            self.conn.write(temp_tag.encode())
            return self.get_out()
        raise "Only ints in range (1,15)"

    def retry(self,retry_times):
        if retry_times in range(0,254):
            temp_tag = self.tag+f"+RETRY={retry_times}"
            self.conn.write(temp_tag.encode())
            return self.get_out()
        raise "Only ints in range (0,254)"

    def rxwin2(self,query=None):
        if query == None:
            temp_tag = self.tag+f"+RXWIN2"
        else:
            temp_tag = self.tag+f"+RXWIN2={query}"
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def rxwin1(self,query=None):
        if query == None:
            temp_tag = self.tag+f"+RXWIN1"
        else:
            temp_tag = self.tag+f"+RXWIN1={query}"
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def key(self,type_key,hex_key):
        check_hex_from(hex_key)
        if type_key.upper() in ["APPSKEY","NWSKEY"]:
            temp_tag = self.tag+f'+KEY={type_key}, "{hex_key}"'
            return self.get_out()
        raise "Invalid key type APPSKEY,NWSKEY"

    def fdefault(self,Seeed=False):
        temp_tag = self.tag+f'+FDEFAULT'
        if Seeed == True:
            temp_tag += "=Seeed"
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def dfu(self,mode):
        if mode == "?":
            temp_tag = self.tag+f'+DFU=?'
        elif mode.upper() == "ON":
            temp_tag = self.tag+f'+DFU=ON'
        elif mode.upper() == "OFF":
            temp_tag = self.tag+f'+DFU=OFF'
        else:
            raise "Mode avalable On,Off,?"
        self.conn.write(temp_tag.encode())
        return self.get_out()


    def set_mode(self,mode = None):
        if mode == None:
            temp_tag = self.tag+f'+MODE'
            self.conn.write(temp_tag.encode())
            for i in range(2):
                self.get_out()
            return self.get_out()
        elif mode.upper() in ["TEST","LWOTAA","LWABP"]:
            temp_tag = self.tag+f'+MODE={mode.upper()}'
            self.conn.write(temp_tag.encode())
            for i in range(2):
                self.get_out()
            return self.get_out()
        else:
            raise "Modes avalable TEST,LWOTAA,LWABP"

    def join(self,query=None):
        if query == None:
            temp_tag = self.tag+f"+JOIN"
        else:
            temp_tag = self.tag+f"+JOIN={query}"
        self.conn.write(temp_tag.encode())
        out_put = []
        for i in range(4):
            try:
                i = self.get_out()
                if i not in [b'+INFO: Input timeout\r\n',b'\r\n']:
                    out_put.append(i)
            except:
                return out_put
        return out_put

    def beacon(self,query=None):
        if query == None:
            temp_tag = self.tag+f"+BEACON"
        else:
            temp_tag = self.tag+f"+BEACON={query}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def set_class(self,c_info=None,saver=False):
        temp_tag = self.tag+f"+CLASS"
        if c_info != None:
            if c_info.upper() in ["A","B","C"]:
                temp_tag += "="+c_info.upper()
            else:
                raise ""
        if saver == True:
            temp_tag += ",SAVE"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def delay(self,rx=None,ms=None):
        temp_tag = self.tag+f"+DELAY"
        if rx != None:
            if rx.upper() in ["RX1","RX2","JRX1","JRX2"]:
                temp_tag += f"={rx.upper()}"
            else:
                raise 'Only in "RX1","RX2","JRX1","JRX2"'
        if ms != None and rx != None:
            temp_tag += f", {ms}"
        elif ms != None:
            raise "NAO SEIJAS OTARIO"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def lw(self,query=None):
        temp_tag = self.tag+f"+LW"
        if query != None:
            temp_tag += f"={query}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def wdt(self,set=None):
        temp_tag = self.tag+"+WDT"
        if set != None:
            if set.upper() in ["ON","OFF"]:
                temp_tag += f"={set.upper()}"
            else:
                raise "ON OR OFF"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def lowpower(self,var):
        temp_tag = self.tag+"+LOWPOWER"
        if type(var) == type(int()):
            temp_tag += f"={var}"
        elif var.lower() == "autoon":
            temp_tag += f"=AUTOON"
        elif var.lower() == "autooff":
            temp_tag += f"=AUTOOFF"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def voltagem(self):
        temp_tag = self.tag + "+VDD"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def rtc(self,opt=None):
        temp_tag = self.tag + "+RTC"
        if opt != None:
            temp_tag += f"={opt}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def eeprom(self,opt=None):
        temp_tag = self.tag + "+EEPROM"
        if opt != None:
            temp_tag += f"={opt}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def uart(self,opt=None):
        temp_tag = self.tag + "+UART"
        if opt != None:
            temp_tag += f"={opt}"
        self.conn.write(temp_tag.encode())
        for i in range(2):
            self.get_out()
        return self.get_out()

    def test(self,opt=None):
        temp_tag = self.tag + "+TEST"
        if opt != None:
            temp_tag += f"={opt}"
        self.conn.write(temp_tag.encode())
        out_put = []
        if 'TXLRPKT' in opt or 'RXLRPKT' in opt:
            for i in range(2):
                i = self.get_out()
                if i not in [b'+INFO: Input timeout\r\n',b'\r\n',b'+TEST: RXLRPKT\r\n',None]:
                    out_put.append(i)
            return out_put
        elif 'RFCFG' in opt:
            for i in range(3):
                i = self.get_out()
                if i not in [b'+INFO: Input timeout\r\n',b'\r\n']:
                    out_put.append(i)
            return out_put
            #return self.get_out()
        for i in range(4):
            try:
                i = self.get_out()
                if i not in [b'+INFO: Input timeout\r\n',b'\r\n',b'+TEST: RXLRPKT\r\n',None]:
                    out_put.append(i)
            except:
                return out_put
        return out_put
    def log(self,opt=None):
        temp_tag = self.tag + "+LOG"
        if opt != None:
            temp_tag += f"={opt}"
        self.conn.write(temp_tag.encode())
        return self.get_out()

    def reset(self):
        temp_tag = self.tag+"+RESET"
        self.conn.write(temp_tag.encode())
        return self.get_out()
