import calendar
from tabulate import tabulate
import colorama

colorama.init(autoreset=True)  # Alustaa coloraman

# Määritellään oikea tiedoston nimi
TIEDOSTO = "kalenteri.txt"

# Valikko, käyttäjä voi valita haluamansa toiminnon
def valikko(): 
    # Looppi, jotta ohjelma pyörii, kunnes käyttäjä valitsee lopettaa
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
            tapahtumat = lue_tapahtumat()
            tarkastelu(vuosi, kuukausi, tapahtumat)
        elif valinta == 2:
            tapahtuman_lisäys()
        elif valinta == 3:
            poista_tapahtuma()
        elif valinta == 4:
            muokkaa_tapahtumaa()
        elif valinta == 5:
            print("-" * 36)
            print('Ohjelma suljetaan. Kiitos käytöstä!')
            print("-" * 36)
            break

# Lukee tapahtumat tiedostosta ja lisää ne listalle
def lue_tapahtumat():
    tapahtumat = {} # Kerätään tapahtumat
    try:
        with open(TIEDOSTO, "r") as file: # Avataan tiedosto lukutilassa
            for rivi in file: # Käydään läpi rivi kerrallaan
                try:
                    osat = rivi.strip().split(", ") # Pilkotaan rivi pilkkujen ja välilyöntien kohdalta
                    if len(osat) == 5: # Varmistetaan, että on oikea määrä osia
                        vuosi, kuukausi, päivä, kellonaika, kuvaus = osat # Nimetään osat
                        try:
                            vuosi, kuukausi, päivä = int(vuosi), int(kuukausi), int(päivä) # Muutetaan kokonaisluvuiksi
                            tapahtumat.setdefault((vuosi, kuukausi), []).append((päivä, kellonaika, kuvaus)) # Lisätään tapahtuma sanakirjaan niin, että vuodella ja kuukaudella on oma lista
                        except ValueError:
                            print(f"Virheellinen tieto rivillä: {rivi.strip()} ohitetaan")
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
    tapahtuma_lista = tapahtumat.get((vuosi, kuukausi), []) # Lista päivä + kuvaus pareista
    tapahtuma_paivat = {päivä for (päivä, _, _) in tapahtuma_lista}
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

    if tapahtuma_lista:
        print("\nTapahtumat tässä kuussa:")
        for päivä, kellonaika, kuvaus in sorted(tapahtuma_lista):
            print(f"- {päivä}. päivä: {kuvaus} kello: {kellonaika}")
    else:
        print("Ei tapahtumia tässä kuussa.")


# Lisää tapahtuman tiedostoon kalenteri.txt
def tapahtuman_lisäys():
    
    try:
        vuosi = int(input("Kerro vuosi: ")) 
        kuukausi = int(input("Kerro kuukausi: ")) # Kerätään käyttäjältä tiedot vuodesta, kuukaudesta ja päivästä
        päivä = int(input("Kerro päivä: "))
        kellonaika = (input("Kerro kellonaika (HH:MM): "))

        if not kellonaika.count(":") == 1 or not all(x.isdigit() for x in kellonaika.split(":")): # Tarkistetaan, että kellonaika on oikeassa muodossa
            print("Virheellinen kellonaika. Käytä muotoa HH:MM. ")
            return
        tapahtuman_kuvaus = (input("Kerro tapahtuman nimi: "))
        tietue = f"{vuosi}, {kuukausi}, {päivä}, {kellonaika}, {tapahtuman_kuvaus}" # Talletetaan tiedot muuttujaan tietue

        with open(TIEDOSTO, "a") as file:
            file.write(tietue + "\n") # Kirjoitetaan tiedostoon haluttu tietue + rivinvaihto
            print("\nTapahtuma tallennettu onnistuneesti. ")
    except ValueError: # Virhe, jos käyttäjä syöttää muuta, kuin kokonaislukuja
        print("Virheellinen syöte. Anna numerot vuodelle, kuukaudelle ja päivälle.")

    except ValueError:
        print("Anna numerot vuodelle, kuukaudelle ja päivälle.")

# Käyttäjä syöttää halutun tapahtuman ja se poistetaan ///KESKEN! //Ei toimi kunnolla

def poista_tapahtuma():
    try:
        infile = open('kalenteri.txt', 'r')
        tapahtumat = infile.readlines()

        if not tapahtumat:
            print("Kalenteri on tyhjä.")
            return

        hakusana = input("Anna poistettavan tapahtuman nimi tai osa siitä: ").strip().lower()
        osumat = [(i, rivi) for i, rivi in enumerate(tapahtumat) if hakusana in rivi.lower()]

        if not osumat:
            print("Ei löytynyt vastaavia tapahtumia.")
            return

        print("Löytyneet tapahtumat:")
        for idx, (i, rivi) in enumerate(osumat, 1):
            print(f"{idx}. {rivi.strip()}")

        valinta = int(input("Valitse poistettava tapahtuma (numero): "))
        if 1 <= valinta <= len(osumat):
            indeksi_poistettava = osumat[valinta - 1][0]
            poistettava = tapahtumat.pop(indeksi_poistettava)
            with open("kalenteri.txt", "w", encoding="utf-8") as tiedosto:
                tiedosto.writelines(tapahtumat)
            print(f"Tapahtuma poistettu: {poistettava.strip()}")
        else:
            print("Virheellinen valinta.")
    except FileNotFoundError:
        print("Kalenteritiedostoa ei löytynyt.")
    except ValueError:
        print("Syötä kelvollinen numero.")
#def poista_tapahtuma(vuosi, kuukausi, tapahtumat):

    #try:
        #with open(TIEDOSTO, "a") as file:
            #for event in file:
                #if event == tapahtumat:
                    #event = ""
                #else:
                    #print("Päivälle ei ole tapahtumaa.")
    #except FileNotFoundError:
        #print("Tapahtumien haussa kävi virhe") # Error printti, jos tiedostoa ei löydy
    #except Exception as e:
        #print(f"Odottamaton virhe: {e}") # Error printti muihin virheisiin
    #except OSError as e:
        #print(f"Virhe tiedostoon kirjoittamisessa: {e}") # Virheilmoitus muille tiedostovirheille

def muokkaa_tapahtumaa():
    try:
        infile = open("kalenteri.txt", "r") #Avataan tiedosto lukutilassa
        tapahtumat = infile.readlines()

        if not tapahtumat:
            print("Kalenteri on tyhjä.")
            return

        hakusana = input("Anna muokattavan tapahtuman nimi tai osa siitä: ").strip().lower() #Käyttäjä syöttää hakusanan
        osumat = [(i, rivi) for i, rivi in enumerate(tapahtumat) if hakusana in rivi.lower()]

        if not osumat:
            print("Ei löytynyt vastaavia tapahtumia.")
            return

        print("Löytyneet tapahtumat:")
        for idx, (i, rivi) in enumerate(osumat, 1):
            print(f"{idx}. {rivi.strip()}")

        valinta = int(input("Valitse muokattava tapahtuma (numero): "))
        if 1 <= valinta <= len(osumat):
            indeksi_muokattava = osumat[valinta - 1][0]
            vanha = tapahtumat[indeksi_muokattava].strip()
            uusi_pvm = input("Anna uusi päivämäärä (YYYY-MM-DD): ").strip()
            uusi_kuvaus = input("Anna uusi tapahtuman kuvaus: ").strip()
            tapahtumat[indeksi_muokattava] = f"{uusi_pvm};{uusi_kuvaus}\n"

            with open("kalenteri.txt", "w", encoding="utf-8") as tiedosto:
                tiedosto.writelines(tapahtumat)

            print(f"Tapahtuma päivitetty:\nVanha: {vanha}\nUusi: {tapahtumat[indeksi_muokattava].strip()}")
        else:
            print("Virheellinen valinta.")
    except FileNotFoundError:
        print("Kalenteritiedostoa ei löytynyt.")
    except ValueError:
        print("Syötä kelvollinen numero.")




def main():
    print("-" * 33)
    print("Tervetuloa käyttämään kalenteria! ")
    print("-" * 33)
    
    valikko()

if __name__ == "__main__":
    main()