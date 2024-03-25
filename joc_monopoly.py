from monopoly import Jucator
from itertools import cycle
from monopoly import Teren, Start, Gara, Utilitati, Inchisoare

andrei=Jucator(nume="Andrei")
florin = Jucator(nume="Florin")
sabin = Jucator(nume = "Sabin")

jucatori = [andrei, florin, sabin]

masa = [Start(),
        Teren("Timisoara", judet="Timis"), Teren("Lugoj", judet="Timis"), Teren("Faget", judet="Timis"), 
        Teren("Cluj-Napoca", judet="Cluj"), Teren("Turda", judet="Cluj"), Teren("Dej", judet="Cluj"),
        Teren("Severin", judet="Mehedinti", terenuri_in_judet=2), Teren("Orsova", judet="Mehedinti", terenuri_in_judet=2),
        Gara("De Sud"), Gara("De Nord"),
        Utilitati("Apa"), Utilitati("Lumina"),
        Inchisoare()
    ]

def last_man_standing(jucatori: list) -> Jucator:
    castigator =  [jucator for jucator in jucatori if jucator.sold > 0]
    if len(castigator) == 1:
        return castigator[0]

def pozitie_finala(masa: list, jucator: Jucator, pozitii: int) -> int:
    cycle_masa = cycle(masa) # 0
    # jucator.pozitie # 1
    for _ in range(jucator.pozitie):
        next(cycle_masa)

    next(cycle_masa)

    for _ in range(pozitii):
        element = next(cycle_masa)

    return masa.index(element)

# main()

runde = 0
for jucator in cycle(jucatori):
    runde += 1
    if jucator.sold <=0:
        continue
    zar_jucator = jucator.da_cu_zarul()
    
     #pt inchisoare
    if zar_jucator == 0:
        print(f"{jucator} este in inchisoare si nu poate da cu zarul.")
        jucator.in_inchisoare -= 1  # Decrease the prison rounds
        if jucator.in_inchisoare == 0:
            jucator.pozitie = 0  # Move the player to Start after completing the prison rounds
            print(f"{jucator} a iesit din Inchisoare.\n")
        else:
            print(f"{jucator} mai sta {jucator.in_inchisoare} runde in Inchisoare.\n")
        continue  # Skip the rest of the loop for players in prison
    #finish inchisoare
    
    print(f"{jucator} a dat {zar_jucator}")
    pozitie = pozitie_finala(masa, jucator, zar_jucator)
    jucator.pozitie = pozitie
    print(jucator, jucator.pozitie, masa[jucator.pozitie])
    casuta_curent = masa[jucator.pozitie]
    casuta_curent.visit(jucator) 
    winner = last_man_standing(jucatori)
    if winner is not None:
        print(f" Rezultat: {winner} a castigat! dupa {runde}  runde ")
        break
    # if runde == 10:
    #     break   
    
    

    

    
    
    
    

