import calendar
from tabulate import tabulate
import colorama

colorama.init(autoreset=True)  # Alustaa coloraman

# Määritellään oikea tiedoston nimi
TIEDOSTO = "kalenteri.txt"

# Valikko, käyttäjä voi valita haluamansa toiminnon //Ei valmis //Tarvii Try With
def valikko():
    # Looppi, jotta ohjelma pyörii, kunnes käyttäjä valitsee lopettaa ///KESKEN!
    while True:
        # Printit
        print("\nValitse toiminto:")
        print("1. Tarkastele kalenteria")
        print("2. Lisää tapahtuma")
        print("3. Poista tapahtuma")
        print("4. Muokkaa tapahtumaa")
        print("5. Lopeta ohjelma")

        # Tarkastetaan, että käyttäjä syöttää luvun 1-5 väliltä
        while True:
            try:
                valinta = int(input("Valitse toiminto (1-5): ")) # Käyttäjä valitsee numeron, joka vastaa toimintoa
                if valinta in [1, 2, 3, 4, 5]:
                    break # Jos valinta on ok, päästään pois loopista
                else:
                    print("Valitse numero (1-5)")
            except ValueError:
                print("Virheellinen syöte, valitse numero (1-5)")

        if valinta == 1:
            vuosi = int(input("Anna vuosi: "))
            kuukausi = int(input("Anna kuukausi: "))
            tapahtumat = lue_tapahtumat() # Paikanpitäjä tapahtumat // Tähän koodi, joka avaa tekstitiedoston, jossa tallennetut tapahtumat
            tarkastelu(vuosi, kuukausi, tapahtumat)
        elif valinta == 2:
            tapahtuman_lisäys()
        elif valinta == 3:
            poista_tapahtuma()
        elif valinta == 4:
            muokkaa_tapahtumaa()
        elif valinta == 5:
            print('Ohjelma suljetaan. Kiitos käytöstä!')
            break

# Lukee tapahtumat tiedostosta ja lisää ne listalle //vitust kesken
def lue_tapahtumat():
    tapahtumat = {} # Kerätään tapahtumat
    try:
        with open(TIEDOSTO, "r") as file: # Avataan tiedosto lukutilassa
            for rivi in file: # Käydään läpi rivi kerrallaan
                try:
                    osat = rivi.strip().split(", ", 3) # Pilkotaan rivi pilkkujen ja välilyöntien kohdalta
                    if len(osat) == 4: # Varmistetaan, että on oikea määrä osia
                        vuosi, kuukausi, päivä, kuvaus = osat # Nimetään osat
                        vuosi, kuukausi, päivä = int(vuosi), int(kuukausi), int(päivä) # Muutetaan kokonaisluvuiksi
                        tapahtumat.setdefault((vuosi, kuukausi), []).append((päivä, kuvaus)) # Lisätään tapahtuma sanakirjaan niin, että vuodella ja kuukaudella on oma lista
                except ValueError:
                    print(f"Virheelinen rivi: {rivi.strip()} ohitetaan.")
                

    except FileNotFoundError:
        print("Virhe tiedoston hakemisessa.")
    
    return tapahtumat


# Tulostaa kuukausikalenterin ja merkitsee tapahtumapäivät tähdellä (*) //Ehkä toimii about oikein
def tarkastelu(vuosi, kuukausi, tapahtumat):

    # Luodaan kalenteri, jossa viikko alkaa maanantaista
    kalenteri = calendar.TextCalendar(firstweekday=calendar.MONDAY)
    kuukauden_paivat = kalenteri.monthdayscalendar(vuosi, kuukausi)

    # Haetaan tapahtumat annetulle vuodelle ja kuukaudelle
    tapahtuma_paivat = {päivä for (päivä, _) in tapahtumat.get((vuosi, kuukausi), [])}

    # Muokataan kalenterin päivät ja lisätään tähdet tapahtumapäiville
    muokattu_kuukausi = []
    for viikko in kuukauden_paivat: # Käydään läpi viikot
        muokattu_viikko = []
        for paiva in viikko: # Käydään läpi viikonpäivät
            if paiva == 0:  # Tyhjät kohdat kalenterissa ennen kuukauden alkua
                muokattu_viikko.append("")
            elif paiva in tapahtuma_paivat:  # Jos päivälle on tapahtuma
                muokattu_viikko.append(f"{colorama.Fore.RED}{paiva}*{colorama.Style.RESET_ALL}") # Lisätään punainen väri tapahtumapäiville
            else:  # Tavalliset päivät
                muokattu_viikko.append(str(paiva))
        muokattu_kuukausi.append(muokattu_viikko)
    
    # Tulostetaan kalenteri taulukkomuodossa
    otsikot = ["Ma", "Ti", "Ke", "To", "Pe", "La", "Su"]
    print(f"\n{calendar.month_name[kuukausi]} {vuosi}".center(30))
    print(tabulate(muokattu_kuukausi, headers=otsikot, tablefmt="grid"))

# Lisää tapahtuman tiedostoon kalenteri.txt //Ehkä toimii??
def tapahtuman_lisäys():
    try:
        with open(TIEDOSTO, "a") as file: # Avataan tiedosto muokkaus modessa
            print("Tapahtuman lisäys -- esim. 2025 3 07")
            try:
                vuosi = int(input("Kerro vuosi: ")) 
                kuukausi = int(input("Kerro kuukausi: ")) # Kerätään käyttäjältä tiedot vuodesta, kuukaudesta ja päivästä
                päivä = int(input("Kerro päivä: "))
            except ValueError: # Virhe, jos käyttäjä syöttää muuta, kuin kokonaislukuja
                print("Virheellinen syöte. Anna numerot vuodelle, kuukaudelle ja päivälle.")
            tapahtuman_kuvaus = (input("Kerro tapahtuman nimi: "))
            tietue = f"{vuosi}, {kuukausi}, {päivä}, {tapahtuman_kuvaus}" # Talletetaan tiedot muuttujaan tietue
            file.write(tietue + "\n") # Kirjoitetaan tiedostoon haluttu tietue + rivinvaihto
            print("\nTapahtuma tallennettu onnistuneesti. ")
    except FileNotFoundError:
        print("Tapahtumien haussa kävi virhe") # Error printti, jos tiedostoa ei löydy
    except Exception as e:
        print(f"Odottamaton virhe: {e}") # Error printti muihin virheisiin
    except OSError as e:
        print(f"Virhe tiedostoon kirjoittamisessa: {e}") # Virheilmoitus muille tiedostovirheille

# Käyttäjä syöttää halutun tapahtuman ja se poistetaan ///KESKEN! //Ei toimi kunnolla
def poista_tapahtuma(vuosi, kuukausi, tapahtumat):

    try:
        with open(TIEDOSTO, "a") as file:
            for event in file:
                if event == tapahtumat:
                    event = ""
                else:
                    print("Päivälle ei ole tapahtumaa.")
    except FileNotFoundError:
        print("Tapahtumien haussa kävi virhe") # Error printti, jos tiedostoa ei löydy
    except Exception as e:
        print(f"Odottamaton virhe: {e}") # Error printti muihin virheisiin
    except OSError as e:
        print(f"Virhe tiedostoon kirjoittamisessa: {e}") # Virheilmoitus muille tiedostovirheille






def main():
    print("-" * 33)
    print("Tervetuloa käyttämään kalenteria! ")
    print("-" * 33)
    
    valikko()

if __name__ == "__main__":
    main()
