import threading
import time

sillas = threading.Semaphore(4)
barberoListo = threading.Semaphore(1)
clienteListo = threading.Semaphore(1)
corteTerminado = threading.Semaphore(1)

sillasDisponibles = 4
TotalClientes = 0

def corteFinalizado():
    print('\nCorte terminado\n')
    corteTerminado.release()

def cortarCabello():
    print('Cortando el cabello...')
    time.sleep(3)
    corteFinalizado()

def funcionBarbero():
    #Trabajará siempre y cuando haya clientes esperando
    global TotalClientes
    while TotalClientes == 0:
        print('No hay clientes. El barbero duerme tranquilamente...')
        #time.sleep(2)
    while TotalClientes > 0:
        #Espera a que llegue un cliente
        clienteListo.acquire()
        global sillasDisponibles 
        print('\nEl barbero recibe solicitud del cliente y lo atiende')
        #Permite que el número de sillas disponibles incremente
        sillasDisponibles += 1
        sillas.release()
        print('Sillas disponibles: ', sillasDisponibles)
        print('Total de clientes (sumando al que está siendo atendido): ', TotalClientes)
        #Y ahora sí, corta el cabello
        cortarCabello()
        #Una vez terminó de cortar el cabello, está listo para ir con el siguiente cliente
        barberoListo.release()
        TotalClientes -= 1
    

def funcionCliente(index):
    #Primero llega a la tienda y observa si hay sillas disponibles
    print('\nLlega cliente: ', index)
    global sillasDisponibles
    if(sillasDisponibles>0):
        #Toma una silla
        sillas.acquire()
        sillasDisponibles -= 1
        global TotalClientes
        TotalClientes += 1
        print('El cliente se sienta en una silla')
        print('El cliente indica que está listo para recibir el corte')
        print('Sillas disponibles: ', sillasDisponibles)
        print('Total de clientes (sumando al que está siendo atendido): ', TotalClientes)
        clienteListo.release()
        #Espera a que el barbero esté listo para realizar el siguiente corte
        corteTerminado.acquire()
        barberoListo.acquire()
        #Finalmente, le cortan el cabello
    
    #Si no hay sillas disponibles, se va de la tienda
    else:
        print('\nEl cliente se va de la tienda al ver que no hay asientos disponibles')

def main():
    #band = True
    while True:
        print("Cuando el programa finalice, por favor indique si le gustaría repetirlo. (s/n)")
        barbero = threading.Thread(target=funcionBarbero)
        num = int(input("Indique el número de clientes que llegarán a la tienda: "))
        
        barbero.start()
        listaClientes = list()
        for index in range(num):
            c = threading.Thread(target=funcionCliente, args=(index+1,))
            listaClientes.append(c)
            time.sleep(1)
            c.start()
        time.sleep(3*num)
        value = input('¿Deseas repetir el programa? s/n.\n')
        if(value == "n" or value == "N"):
            break

if __name__ == '__main__':
   main()