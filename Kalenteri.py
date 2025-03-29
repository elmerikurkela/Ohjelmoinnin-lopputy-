import calendar
from tabulate import tabulate

# Valikko, käyttäjä voi valita haluamansa toiminnon
def valikko():
    filename = "kalenteri.txt" # Määritellään oikea tiedoston nimi
    # Looppi, jotta ohjelma pyörii, kunnes käyttäjä valitsee lopettaa ///KESKEN!
    while True:
        # Printit
        print("Tervetuloa käyttämään kalenteria! ")
        print("\nValitse toiminto:")
        print("1. Tarkastele kalenteria")
        print("2. Lisää tapahtuma")
        print("3. Poista tapahtuma")
        print("4. Muokkaa tapahtumaa")
        print("5. Lopeta ohjelma")
        valinta = input("Valitse toiminto (1-5):") # Käyttäjä valitsee numeron, joka vastaa toimintoa

        if valinta == 1:
            vuosi = int(input("Anna vuosi: "))
            kuukausi = int(input("Anna kuukausi: "))
            tapahtumat = [1, 10, 20] # Paikanpitäjä tapahtumat // Tähän koodi, joka avaa tekstitiedoston, jossa tallennetut tapahtumat
            tarkastelu(vuosi, kuukausi, tapahtumat)
        elif valinta == 2:
            tapahtuman_lisäys(vuosi, kuukausi, tapahtumat)
        else:
            print("Valitse numero (1-5)")
            
        



# Tulostaa kuukausikalenterin ja merkitsee tapahtumapäivät tähdellä (*)
def tarkastelu(vuosi, kuukausi, tapahtumat):

    # Luodaan kalenteri, jossa viikko alkaa maanantaista
    kalenteri = calendar.TextCalendar(firstweekday=calendar.MONDAY)
    kuukauden_paivat = kalenteri.monthdayscalendar(vuosi, kuukausi)

    # Muokataan kalenterin päivät ja lisätään tähdet tapahtumapäiville
    muokattu_kuukausi = []
    for viikko in kuukauden_paivat:
        muokattu_viikko = []
        for paiva in viikko:
            if paiva == 0:  # Tyhjät päivät
                muokattu_viikko.append("")
            elif paiva in tapahtumat:  # Tapahtumapäivät
                muokattu_viikko.append(f"{paiva}*")
            else:  # Tavalliset päivät
                muokattu_viikko.append(str(paiva))
        muokattu_kuukausi.append(muokattu_viikko)
    
    # Tulostetaan kalenteri taulukkomuodossa
    otsikot = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    print(f"\n{calendar.month_name[kuukausi]} {vuosi}".center(30))
    print(tabulate(muokattu_kuukausi, headers=otsikot, tablefmt="grid"))

# Lisää tapahtuman tiedostoon kalenteri.txt
def tapahtuman_lisäys(vuosi, kuukausi, paiva):
    filename = "kalenteri.txt"
    try:
        with open(filename, "a") as file: # Avataan tiedosto muokkaus modessa
            print("-" * 20) # Printataan raamia
            print("Tapahtuman lisäys -- esim. 2025 3 07")
            tietue = input("\nKerro vuosi, kuukausi ja päivä: ")
            print("-" * 20) # Printataan raamia
            file.write(tietue + "\n") # Kirjoitetaan tiedostoon haluttu tietue + rivinvaihto
            print("\nTapahtuma tallennettu onnistuneesti. ")
    except FileNotFoundError:
        print("Tapahtumien haussa kävi virhe") # Error printti, jos tiedostoa ei löydy
    except Exception as e:
        print(f"Odottamaton virhe: {e}") # Error printti muihin virheisiin
    except OSError as e:
        print(f"Virhe tiedostoon kirjoittamisessa: {e}") # Virheilmoitus muille tiedostovirheille




def main():

    filename = "kalenteri.txt"
    
    valikko()

    if __name__ == "__name__":
        main()