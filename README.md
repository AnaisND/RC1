Inainte de inceperea sesiunii se executa fisierul restart.py care construieste sistemul de fisiere local. Autentificarea unui client se face prin comanda login your_secret_. Clientii pot executa doar comenzile listate in meniu dupa autentificare.

Cerinte: Partajarea fisierelor:

Clientul se autentifica prin cont, trimitand server-ului o lista cu fisierele pe care le publica, si primeste lista tuturor fisierelor publicate de catre ceilalti clienti autentificati;

Cand un client se autentifica, ceilalti clienti autentificati primesc o notificare de adaugare a acesuia, impreuna cu lista de fisiere pe care o publica;

Cand un client isi incheie sesiunea cu server-ul, aceste ii confirma incheierea sesiunii si notifica ceilalti clienti autentificati sa stearga din lista clientul respectiv;

Un client poate solicita server-ului descarcarea unui fisier de la alti clienti;

Server-ul solicita detinatorului fisierului respetiv citirea continutului acestuia;

Ulterior, server-ul livreaza continutul fisierului clientului care l-a solicitat;

Clientul salveaza fisierul in sistemul sau de fisiere;

Fiecare client va avea un director gazda expus, care va fi monitorizat;

La adaugarea unui nou fisier in acest director, clientul va notifica prin intermediul server-ului adaugarea fisierului;

La stergerea unui fisier din acest director, clientul va notifica in mod similar ceilalti clienti prin intermediul server-ului.
