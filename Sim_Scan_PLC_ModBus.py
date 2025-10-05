import time
import threading
from pymodbus.client import ModbusTcpClient as MBClient
from timers import TON

#------------------------
# -------- CONFIGURAZIONE 
PLC_IP = "192.168.1.202"
PLC_PORT = 502
INPUT_REGISTER_ADDRESS = 32800

#Indirizzi Modbus 4DO_P
OUTPUT_1, OUTPUT_2, OUTPUT_3, OUTPUT_4 = 32768, 32769, 32770, 32771
#Indirizzi Modbus 4DO_PN_2A
OUTPUT_5, OUTPUT_6, OUTPUT_7, OUTPUT_8 = 32780, 32781, 32782, 32783

utenti = {"Simone Burgio":  {"id": "0F00B18F42", "out": OUTPUT_1},
          "Mario Roxy":     {"id": "909ABF4F", "out": OUTPUT_2 },
          "Ganzo Frozo":    {"id": "AD87B1AB", "out": OUTPUT_3}
          }

# -------------------------------------------
# ----------  DEFINIZIONE MEMORIE DI PROCESSO 
pii = {"status1" : False,
       "status2" : False,
       "status3" : False,
       "s1"      : False}
piq = {"lock1"   : False,
       "lock2"   : False,
       "lock3"   : False,
       "led1"    : False}
step = 0
pc  = {"lock_num": 1}

t1 = TON(preset_time=1)
t2 = TON(preset_time=0.1)


# -----------------------------------
# ---------- SEZIONI LOGICA PROGRAMMA 
def pou1(pii, piq):
     #Accendi il led se una delle serrature è aperta
     if not pii["status1"] or not pii["status2"] or not pii["status3"]:
          print("LED ACCESO")
          piq["led1"] = True
     else:
           piq["led1"] = False

def pou2(pii, piq, pc):
    global step
    
    if step == 0:
        t1(False)  # Reset timer 1
        t2(False)  # Reset timer 2       
        if pii["s1"]:
            step = 1
    
    elif step == 1:
        t2(False)  # Reset timer non in uso
        if t1(True):
            piq["lock1"] = True
            step = 2
    
    elif step == 2:
        t1(False)  # Reset timer non in uso
        
        if t2(True):
            piq["lock1"] = False
            step = 0
              
         
         
# --------------------------
# ---------- TASK PRINCIPALE 

def main_task():

    with MBClient(PLC_IP, port=PLC_PORT) as client:
        if not client.connect():
            print(f"ERRORE: Connessione fallita con {PLC_IP}")
        else:
            print(f"Connessione con {PLC_IP} eseguita")
    
        while True:

            # --- 1: LETTURA INGRESSI E SALVATAGGIO IN MEMORIA
            try:
                    result = client.read_input_registers(address=INPUT_REGISTER_ADDRESS, count=1)
                    register_value = result.registers[0]

                    pii["status1"] = (register_value & 1) != 0
                    pii["status2"] = (register_value & 2) != 0
                    pii["status3"] = (register_value & 4) != 0
                    pii["s1"]      = (register_value & 8) != 0
        
            except Exception as e:
                print(f"Si è verificato un errore durante la lettura: {e}") 
            
            # --- 2: ESECUZIONE LOGICA

            pou1(pii,piq)
            pou2(pii,piq,pc)

            # --- 3: AGGIORNAMENTO USCITE

            client.write_coil(OUTPUT_1, piq["lock1"])
            client.write_coil(OUTPUT_2, piq["lock2"])
            client.write_coil(OUTPUT_3, piq["lock3"])
            client.write_coil(OUTPUT_4, piq["led1"])

            time.sleep(0.1)

if __name__ == "__main__":
     main_task()