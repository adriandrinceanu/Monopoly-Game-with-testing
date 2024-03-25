from random import randrange


class Jucator():
    
    def __init__(self, nume, sold=3000):
        self.nume  = nume
        self.sold = sold 
        self.pozitie = 0 
        self.proprietati =[]
        self.in_inchisoare = 0
        self.runde_in_inchisoare = 0
        
    def da_cu_zarul(self):
        if self.in_inchisoare > 0:
            return 0
        return randrange(2,12)
    
    def __repr__(self):
        return f"<Jucator {self.nume}, sold {self.sold}>"
    
    def iesire_din_joc(self):
        self.in_inchisoare = 0
        self.sold = 0
        for proprietate in self.proprietati:
            proprietate.proprietar = None

    def are_tot_judetul(self, judet) -> bool:
        cartier = [proprietate for proprietate in self.proprietati if hasattr(proprietate, 'judet') and proprietate.judet == judet]
        if len(cartier) > 0:
            return len(cartier) == cartier[0].terenuri_in_judet
        return False
        
class Casuta:  
        
    def visit(self, jucator):
        print(f"{jucator} a ajuns pe {self}\n")
        
class Start(Casuta):
    def __init__(self, nume = "Start"):
        self.nume = nume
        
    def __repr__(self):
        return self.nume
    
    def visit(self, jucator):
        print(f"{jucator} a ajuns pe {self} si va primi 50$\n")
        jucator.sold += 50

class Proprietate(Casuta):
    
    def __init__(self, nume, pret = 500, chirie = 100, ):
        self.nume = nume
        self.pret = pret
        self._chirie = chirie
        self.proprietar = None
        
    def __repr__(self):
        return f"< {self.__class__.__name__},  {self.nume}>"
    
    @property
    def chirie(self):
        return self._chirie
    
    # @property
    # def chirie_hotel(self):
    #     return self._chirie_hotel
    
    def visit(self, jucator: Jucator):
        print(f"{jucator} a ajuns pe {self}")
        if self.proprietar is  None:
            self._cumpara(jucator)
        else:
            self._inchiriaza(jucator)
        
    
    def _cumpara(self, jucator: Jucator):
        if jucator.sold < self.pret:
            print(f"Jucatorul { jucator.nume } nu are bani sa cumpere {self}\n")
            return
        self.proprietar = jucator
        jucator.sold = jucator.sold - self.pret
        jucator.proprietati.append(self)
        print(f"Jucatorul { jucator.nume } a cumparat proprietatea {self.nume}\n")
    
    def _inchiriaza(self, jucator: Jucator):
        if self.proprietar == jucator:
            return
        if jucator.sold - self.chirie > 0:
            self.proprietar.sold += self.chirie    
            jucator.sold = jucator.sold - self.chirie
            print(f"Jucatorul { jucator.nume } plateste chirie lui{self.proprietar}\n")
        # elif jucator.sold - self.chirie_hotel > 0:
        #     self.proprietar.sold += self.chirie_hotel    
        #     jucator.sold = jucator.sold - self.chirie_hotel
        #     print(f"Jucatorul { jucator.nume } plateste chirie pe hotel lui{self.proprietar}\n")
        else:
            self.proprietar.sold += jucator.sold   
            jucator.iesire_din_joc()
            print(f"Jucatorul { jucator.nume } iese din joc\n")

    
class Teren(Proprietate):

    PRET_CASUTA = 50
    PRET_HOTEL = 100
    
    def __init__(self, nume, judet, pret=500, chirie=100, terenuri_in_judet=3):
        super().__init__(nume, pret, chirie)
        self.judet = judet
        self.terenuri_in_judet = terenuri_in_judet
        self.casute = 0
        self.hotel = 0

    def _construieste_casuta(self):
        if self.casute <= 4:
            if self.proprietar.sold > self.PRET_CASUTA:
                self.casute +=1
                self.proprietar.sold -= self.PRET_CASUTA
                print(f"{self.proprietar} a facut o casuta pe {self}\n")
            else:
                print(f"{self.proprietar} nu are bani sa faca o casuta pe {self}\n")
        
        
    def _construieste_hotel(self):        
        if self.hotel <= 4:
            if self.proprietar.sold > self.PRET_HOTEL:
                self.hotel +=1
                self.proprietar.sold -= self.PRET_HOTEL
                print(f"{self.proprietar} a facut un hotel pe {self}\n")
            else:
                print(f"{self.proprietar} nu are bani sa faca un hotel pe {self}\n")

    def visit(self, jucator:Jucator):
        if self.proprietar == jucator and jucator.are_tot_judetul(self.judet):
            self._construieste_casuta()
            
        if self.proprietar == jucator and jucator.are_tot_judetul(self.judet) and self.casute > 4:
            self._construieste_hotel()
        
        super().visit(jucator)

    @property
    def chirie(self):
        if self.hotel >= 1:
            return (self._chirie * self.hotel) + 400
        elif self.casute >= 1 :
            return self._chirie * self.casute
        elif self.casute == 1:
            return self._chirie + 5
        return self._chirie
    
    # @property
    # def chirie_hotel(self):
    #     if self.hotel > 1:
    #         return self._chirie_hotel * self.hotel
    #     elif self.hotel == 1:
    #         return self._chirie_hotel + 50
    #     return self._chirie_hotel
    
        
    

class Gara(Proprietate):
    def __init__(self, nume, pret = 200, chirie = 50):
        super().__init__(nume, pret, chirie)
        self.nume = nume
        self.pret = pret
        # self.chirie = chirie
        self.proprietar = None
        
    
    def __repr__(self):
        return f"{self.__class__.__name__} {self.nume}"
    
    def visit(self, jucator):
        print(f"{jucator} a ajuns pe {self}\n")
        if self.proprietar is  None:
            self._cumpara(jucator)
        else:
            self._inchiriaza(jucator)
            
    @property
    def chirie(self):
        return self._chirie
    

class Utilitati(Proprietate):
    def __init__(self, nume, pret = 100, chirie = 50):
        super().__init__(nume, pret, chirie)

        self.nume = nume
        self.pret = pret
        self.proprietar = None
        
    @property
    def chirie(self):
        return self._chirie
    
    
    def __repr__(self):
        return f"{self.__class__.__name__} {self.nume}"
    
    def visit(self, jucator):
        print(f"{jucator} a ajuns pe {self}\n")
        if self.proprietar is  None:
            self._cumpara(jucator)
        else:
            self._inchiriaza(jucator)
            
    def _inchiriaza(self, jucator):
        self.jucator = jucator
        if self.proprietar == jucator:
            return "Eu sunt proprietarul acestei utilitati"
        rent_amount = jucator.da_cu_zarul() * self.chirie
        if jucator.sold - rent_amount > 0:
            self.proprietar.sold += rent_amount    
            jucator.sold = jucator.sold - rent_amount
            print(f"Jucatorul { jucator.nume } plateste chirie lui {self.proprietar}\n")
        else:
            self.proprietar.sold += jucator.sold   
            jucator.iesire_din_joc()
            print(f"Jucatorul { jucator.nume } iese din joc (lipsa bani pentru utilitati)\n")


class Inchisoare(Casuta):
    def __init__(self, nume = "Inchisore"):
        super().__init__()
        self.nume = nume
        self.in_inchisoare = 3

    def __repr__(self):
            return self.nume


    def visit(self, jucator):
            print(f"{jucator} a ajuns pe {self}")
            if jucator.in_inchisoare == 0:
                print(f"{jucator} este introdus in Inchisoare.")
                print(f"{jucator} mai sta {self.in_inchisoare} runde in Inchisoare.\n")
                jucator.in_inchisoare = self.in_inchisoare



