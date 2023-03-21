import matplotlib.pyplot as plt

class Termostat:

    def __init__(self, items):
        
        self.Kp=float(items['kp'])                      #wzmocnienie regulatora
        self.Ti=float(items['ti'])                       #stała całkowania, zależy czy I czy PI, w PI czas zdwojenia

        self.U_min=0                      #Minimalna wartość sterowania regulatora
        self.U_max=1000                   #Maksymalna wartość sterowania regulatora

        self.tOut=float(items['t_out'])                      #Temperatura na zewnątrz
        self.tIn=self.tOut                #Temperatura we wnątrz
        self.t_target=float(items['t_set'])                  #Temperatura zadana

        self.airSpecificHeat=713          #Ciepło właściwe powietrza
        self.brickThermalCondictivity=0.4 #Przewodnictwo cieplne cegieł
        self.airDensity=1.204             #Gęstość powietrza przy ciśnieniu atmosferycznym
        self.wallThickness=0.24           #Grubość ścian


        self.a=float(items['room_len'])                          #długość, szerokość pokoju
        self.b=float(items['room_hg'])                        #wysokość pokoju
        self.V=self.a*self.a*self.b                      #objętość pokoju 

        self.airMass=self.V*self.airDensity         #Masa powierza wewnątrz pokoju

        self.Tp=0.1                       #okres próbkowania
        self.t_sym=3600                   #czas trwania symulacji


        self.P_min=0                      #W
        self.P_max=6000                   #W

    def heaterPower(self, u_n):        #Moc grzejników
        return max(self.P_max*(u_n)/self.U_max, self.U_min)

    def e_n(self, t_n, t_target):      #uchyb regulacji
        return t_target-t_n

    def u_n(self, e):                  #wielkość sterująca 
        return min(self.Kp*(e[-1]+(self.Tp/self.Ti)*sum(e)), self.U_max)

    def deltaTemperature(self, temp, p):
        c = self.Tp/(self.airMass*self.airSpecificHeat) #stała (delta_t/moc)
        escaping_power = (4*self.a*self.b+2*self.a*self.a) * self.brickThermalCondictivity * (temp-self.tOut) / self.wallThickness
        power = p - escaping_power
        # print("temperatura: {}, grzejnik: {}, ucieczka: {}".format(temp, p, escaping_power))
        del_t = power*c
        return del_t

    def run(self):

        N=int(self.t_sym/self.Tp)
        e=list()
        temp_axis=[]
        time_axis=[]
        p_list=[]

        for n in range(0,N+1):
            e.append(self.e_n(self.tIn, self.t_target))
            u = self.u_n(e)
            self.tIn += self.deltaTemperature(self.tIn, self.heaterPower(u))
            temp_axis.append(self.tIn)
            time_axis.append(n*self.Tp)
            p_list.append(self.heaterPower(u))

        return time_axis, temp_axis, p_list, e

        # plt.figure(figsize=(12,4))

        # plt.subplot(131)
        # plt.plot(time_axis, temp_axis)
        # plt.xlabel("Time [s]")
        # plt.ylabel("Temperature [°C]")
        # plt.title("Temperature Plot")

        # plt.subplot(132)
        # plt.plot(time_axis, p_list)
        # plt.xlabel("Time [s]")
        # plt.ylabel("Heater Power [W]")
        # plt.title("Heater Power Plot")

        # plt.subplot(133)
        # plt.plot(time_axis, e)
        # plt.xlabel("Time [s]")
        # plt.ylabel("Error [°C]")
        # plt.title("Error Plot")

        # plt.tight_layout()
        # plt.show()