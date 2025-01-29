# detect_lunar_flash

Questo tool a linea di comando scritto in <b>Python</b> è pensato per cercare probabili flash da impatto sulla superficie lunare. <br>
Può essere utilizzato in fase di post-processing insieme al software <b>FireCapture</b> (<link>https://www.firecapture.de</link>) unitamente al plugin scritto dal `NOA/ESA` <b>Flash Detection Software</b> (<link>https://kryoneri.astro.noa.gr/en/flash-detection-software/</link>). <br>
Per usare <b>detect_lunar_flash</b> unitamente ad <b>FDS</b>, è necessario salvare i frame dell'eventuale flash come immagini in formato `PNG` (ad esempio 10 frame prima e dopo il flash). <br>
<b>L'orientamento delle immagini deve essere con Nord in alto ed Est a destra.</b><br>
Una volta che è stato rilevato il probabile flash e sono state salvate le <em>n</em> immagini da <b>FDS</b> è possibile utilizzare questo tool per la ricerca dell'eventuale impatto e la determinazione della sua posizione sulla superficie lunare. <br> 
Per la ricerca dei contorni del flash è stato utilizzato l'algoritmo <b>Canny Edge Detector</b> (vedi <link>https://en.wikipedia.org/wiki/Canny_edge_detector</link>)
della libreria `OpenCV`.<br>
Nel caso in cui venga trovato un probabile impatto, viene creata una nuova immagine con un cerchio intorno al flash, che ha il prefisso `flash_`, nella stessa directory da cui vengono lette le immagini (per esempio `flash_1.png`).<br>
Vengono fornite in output le coordinate selenografiche approssimate ed il raggio del probabile flash.

## Prerequisiti

L'unico prerequisito per eseguire il tool è aver installato sul proprio sistema operativo è l'ambiente di virtualizzazione `Docker`. <br>
Il software può essere scaricato da: <link>https://www.docker.com/products/docker-desktop/</link>. <br>
Il link diretto per Windows è: <a href="https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=module&_gl=1*1pd78qm*_gcl_au*MTEzNjQ4MDQwNS4xNzM4MDY4NDQ2*_ga*MTg2ODU3OTU3MC4xNzM0NDI1MjM4*_ga_XJWPQMJYHQ*MTczODE0NDI4OS40LjEuMTczODE0ODI0OC41OS4wLjA">questo</a>.

## Installazione (tramite immagine Docker)
Questo metodo deve essere utilizzato nel caso non si vogliano i sorgenti ed è il <b>metodo da utilizzare nella maggior parte dei casi</b>. <br>
Da una shell Windows/Linux/macOS eseguire il seguente comando:

```
docker pull eugeniopolito/detect_lunar_flash   
```

## Installazione (tramite sorgenti)
In alternativa il tool può essere installato attraverso i sorgenti in questo modo:
- scaricare il codice sorgente da `GitHub` direttamente da console col comando: 
 ```
git clone https://github.com/eugeniopolito/detect_lunar_flash.git
```
oppure cliccando sul bottone verde `< > Code` e selezionando quindi `Download ZIP`.

- eseguire i seguenti comandi:

```
cd detect_lunar_flash
 
docker build -t detect_lunar_flash .  
```

## Avvio del tool
Per eseguire il programma lanciare il seguente comando nel caso in cui l'installazione è stata fatta tramite l'immagine `Docker`:

```
docker run --rm -v <directory>:/app/images -it eugeniopolito/detect_lunar_flash
```

nel caso invece si è proceduto con l'installazione e la build dei sorgenti, eseguire il comando:

```
docker run --rm -v <directory>:/app/images -it detect_lunar_flash
```

dove `<directory>` è la directory del proprio file system che contiene le immagini in formato `PNG` da analizzare. Per esempio: `c:\immagini` (Windows) oppure `/home/user/images` (macOS/Linux). <br>
In questa directory verranno eventualmente scritte le immagini in cui vengono trovati i probabili flash.


## Esempio

Dopo l'avvio, il tool si presenta così:

```
------------------------
detect_lunar_flash
v. 0.1
Eugenio Polito
Copyright © 2025
------------------------
Inserisci la dimensione del pixel della camera (µm)
[ZWO: ASI 224 = 3.75, ASI 178 = 2.4, ASI 120 = 3.75, ASI 290 = 2.9]
[Player One: Neptune-C II = 2.9]
-->
```

Il primo parametro richiesto è la dimensione del pixel del sensore della camera utilizzata per le riprese. Sono riportate quelle di uso più comune ma è facile trovare su Google le dimensioni per altri sensori.<br>
Questo parametro, insieme alla lunghezza focale e al fattore di moltiplicazione della lente di Barlow/riduttore, servono per calcolare il fattore di scala per la ricerca delle coordinate selenografiche e per la stima della dimensione del flash. <br>
Il secondo prompt è quindi:
```
Inserisci la focale nativa del telescopio (mm)
[1000, 2000, ...]
-->
```

E poi:

```
Inserisci il fattore di scala della lente di Barlow
[1 = Nessuna lente, 0.3, 0.5, 2, ...]
```

Per esempio con i valori: `3.75`, `2000`, `0.3` si ottiene questo output:

```
Il fattore di scala calcolato è [km/pixel]: 2.41
```

Il programma passa quindi ad elaborare tutti i file contenuti nella directory `<directory>` passata come argomento in fase di avvio. <br>
Nel caso venga trovato effettivamente un probabile flash, l'output del programma è questo:

```
***ATTENZIONE: Probabile flash trovato in '/Users/eugenio/test_impact_images/frame_009.png'!***


Punto più luminoso (pixel): (157, 1004)
Centro stimato (pixel): (671.58, 694.72)
Raggio stimato [km]: 11.55
Latitudine: -25.39°N
Longitudine: -52.14°E
```

e nella directory delle immagini viene prodotto il file col marcatore del flash `flash_1.png`.<br>
Nel caso in cui non vengano trovati dei flash, il tool non fornisce alcun output.

## Licenza

This program is free software.
It is licensed under the GNU GPL version 3 or later.
That means you are free to use this program for any purpose;
free to study and modify this program to suit your needs;
and free to share this program or your modifications with anyone.
If you share this program or your modifications
you must grant the recipients the same freedoms.
To be more specific: you must share the source code under the same license.
For details see <link>https://www.gnu.org/licenses/gpl-3.0.html</link>


