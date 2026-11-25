---
title: "EcoSync: Distribuirani digitalni blizanac i sistem za optimizaciju resursa u realnom vremenu za energetske mreže pametnih gradova"
subtitle: "Sistemska arhitektura, matematički modeli optimizacije, dvostruki tokovi telemetrije i testovi otpornosti"
author: "Nikola Marović"
institute: "Primenjeno softversko inženjerstvo u infrastrukturnim sistemima — Fakultet tehničkih nauka (FTN), Univerzitet u Novom Sadu"
date: "2026"
version: "1.0.0"
keywords: [Digital Twin, Smart Grid, Distribuirani sistemi, .NET Core, TimescaleDB, Redis, MQTT, gRPC, Linearno programiranje, SCADA, Chaos Engineering]
---

# Izvršni rezime (Executive Abstract)

Ubrzana integracija nestabilnih obnovljivih izvora energije — kao što su solarni parkovi i vetroelektrane — u gradske elektroenergetske mreže uvodi ozbiljne izazove u sinhronizaciji proizvodnje i potrošnje. Za razliku od upravljivih termoelektrana, proizvodnja iz obnovljivih izvora stohastički varira u zavisnosti od meteoroloških uslova, što često dovodi do naglih večernjih deficita energije i primorava operatere mreže da aktiviraju skupe vršne elektrane na fosilna goriva sa visokom emisijom ugljen-dioksida ($CO_2$). Tradicionalni SCADA (*Supervisory Control and Data Acquisition*) sistemi ostaju pretežno pasivni i pružaju vizuelizaciju u realnom vremenu bez prediktivnog balansiranja opterećenja i automatizovanog upravljanja baterijskim skladištima.

**EcoSync** rešava ovaj problem kroz distribuiranu, na otkaze otpornu platformu **digitalnog blizanca** (*Digital Twin*) i sistema za optimizaciju resursa projektovanu na nivou makro-infrastrukture. Umesto modelovanja fizike niskonaponskih električnih kola i elektromagnetizma, EcoSync apstrahuje urbani energetski ekosistem u dinamičke gradske zone potrošnje, stohastičke klastere obnovljive proizvodnje i baterijske sisteme za skladištenje energije velikog kapaciteta (*Energy Storage Systems — ESS*).

Platforma je arhitektonski podeljena u šest međusobno razdvojenih inženjerskih faza:
1. **IoT Edge makro-simulacija:** Generator telemetrije napisan u jeziku `Python` koji u podsekundnim intervalima strimuje podatke o potrošnji grada, proizvodnji iz obnovljivih izvora i stanju napunjenosti baterija ($SoC$) preko `MQTT` protokola koristeći binarni format `Protocol Buffers (Protobuf)`.
2. **High-Load Core Backend i dvostruko skladištenje podataka:** Višenitni C# (`.NET Core`) server za prijem podataka koji implementira arhitekturu vruće i hladne putanje (*Hot/Cold storage split*) — trenutno operativno stanje upisuje se u **Redis** radi očitavanja u vremenu ispod jedne milisekunde, dok se istorijski podaci vremenskih serija asinhrono perzistiraju u **PostgreSQL / TimescaleDB** hipertabele (*hypertables*).
3. **Prediktivni i preskriptivni AI modul:** `Python` mikroservis povezan preko **gRPC** protokola koji kombinuje `scikit-learn` modele mašinskog učenja za prognozu potrošnje sa **linearnim programiranjem** (`SciPy` / `Google OR-Tools`) radi izračunavanja optimalnog rasporeda punjenja i pražnjenja baterija sa ciljem minimizacije emisije $CO_2$.
4. **SCADA komandni centar:** Interaktivna operaterska konzola tamne teme razvijena u tehnologijama `Next.js` i `TypeScript`, pogonjena dvosmernom komunikacijom u realnom vremenu putem `SignalR` WebSocket kanala.
5. **Terenski i menadžerski mobilni interfejs:** `React Native` mobilna aplikacija za isporuku kritičnih alarma o deficitu zelene energije i autorizovano daljinsko odobravanje rezervnih kapaciteta.
6. **Otpornost, observabilnost i sajber-bezbednost:** Testiranje opterećenja i inženjering haosa (*Chaos Engineering*) pomoću alata `k6`, nadzor infrastrukturnih metrika u realnom vremenu kroz `Prometheus` i `Grafana` alate, automatizovano definisanje cloud infrastrukture putem `Terraform`-a i zaštita API sloja primenom JWT autentifikacije i ograničavanja protoka (*Rate Limiting*).

Arhitektonski ciljevi sistema podrazumevaju održivi protok prijema podataka veći od $10.000\text{ poruka/sekundi}$ uz ukupnu latenciju obrade ispod $15\text{ ms}$ ($p99$), čime se u simuliranim uslovima postiže smanjenje aktivacije vršnih elektrana na fosilna goriva za $18\% - 25\%$.

---

## Indeks poglavlja (Whitepaper Chapter Index)

> **Napomena za generisanje PDF-a:** Prilikom kompajliranja u PDF format putem alata Pandoc i XeLaTeX, automatski paginirani Sadržaj, Lista slika i Lista tabela generišu se neposredno nakon ove sekcije. Za direktnu navigaciju na GitHubu koristite linkove ka poglavljima u tabeli ispod:

| Poglavlje | Fajl dokumentacije | Ključni inženjerski opseg |
| :--- | :--- | :--- |
| **00** | [`00_Abstract_and_TOC.md`](./00_Abstract_and_TOC.md) | Izvršni rezime, metapodaci dokumenta i rečnik skraćenica |
| **01** | [`01_Vision_and_Context.md`](./01_Vision_and_Context.md) | Definicija problema (*Duck Curve*), makro-jednačine bilansa, C4 kontekst i KPI |
| **02** | [`02_System_Architecture.md`](./02_System_Architecture.md) | C4 topologija kontejnera i komponenti, mrežni protokoli i dijagrami sekvenci |
| **03** | [`03_Phase1_Edge_Sim.md`](./03_Phase1_Edge_Sim.md) | Jednačine stohastičke simulacije, MQTT teme, QoS nivoi i Protobuf šeme |
| **04** | [`04_Phase2_Core_Backend.md`](./04_Phase2_Core_Backend.md) | .NET konkurentni kanali, Redis keširanje, TimescaleDB hipertabele i CI/CD |
| **05** | [`05_Phase3_AI_Predict.md`](./05_Phase3_AI_Predict.md) | Inženjering obeležja vremenskih serija, ML regresija, linearno programiranje i gRPC |
| **06** | [`06_Phase4_SCADA_Web.md`](./06_Phase4_SCADA_Web.md) | Next.js SCADA interfejs, baferovanje SignalR stanja i optimizacija rendera |
| **07** | [`07_Phase5_Field_App.md`](./07_Phase5_Field_App.md) | React Native mobilni tokovi, isporuka push alarma i bezbednosni protokoli |
| **08** | [`08_Phase6_Resilience.md`](./08_Phase6_Resilience.md) | k6 stres/haos testovi, Prometheus/Grafana observabilnost i Terraform IaC |
| **10** | [`10_ADR_Log.md`](./10_ADR_Log.md) | Dnevnik arhitektonskih odluka (ADR) sa analizom tehničkih kompromisa |
| **11** | [`11_Literature.md`](./11_Literature.md) | Akademska literatura, specifikacije protokola i industrijski standardi |

---

## Nomenklatura i rečnik skraćenica

| Akronim | Pun naziv (eng.) | Kontekst u EcoSync arhitekturi |
| :--- | :--- | :--- |
| **ADR** | Architecture Decision Record | Strukturisani zapis koji dokumentuje kontekst, razmatrane alternative i kompromise ključnih arhitektonskih odluka |
| **BMS** | Battery Management System | Podsistem na ivici mreže koji izveštava o napunjenosti baterije ($SoC\%$), temperaturi i limitima punjenja |
| **CI/CD** | Continuous Integration / Continuous Deployment | Automatizovani pipeline za izgradnju, testiranje i verifikaciju kontejnera putem GitHub Actions servisa |
| **ESS** | Energy Storage System | Gradske baterijske banke velikog kapaciteta za peglanje vršnog opterećenja i skladištenje viška zelene energije |
| **gRPC** | Google Remote Procedure Call | Binarni RPC radni okvir visokih performansi koji povezuje C# jezgro i Python AI servis |
| **IaC** | Infrastructure as Code | Deklarativno definisanje i podizanje cloud resursa korišćenjem alata Terraform |
| **JWT** | JSON Web Token | Kriptografski standard tokena za zaštitu REST i WebSocket krajnjih tačaka operatera |
| **KPI** | Key Performance Indicator | Merljivi ciljevi latencije, propusne moći, dostupnosti i ekološke efikasnosti sistema |
| **LP** | Linear Programming | Matematička metoda optimizacije koja minimizuje emisiju $CO_2$ uz poštovanje fizičkih ograničenja mreže |
| **MAPE** | Mean Absolute Percentage Error | Statistička metrika tačnosti kojom se ocenjuje greška ML modela za prognozu potrošnje |
| **MQTT** | Message Queuing Telemetry Transport | Lagani *publish/subscribe* protokol za razmenu poruka sa IoT edge uređajima |
| **p99** | 99th Percentile Latency | Gornja granica vremena obrade unutar koje se uspešno završi $99\%$ svih telemetrijskih paketa |
| **Protobuf** | Protocol Buffers | Kompaktan binarni format serijalizacije koji smanjuje mrežni saobraćaj u poređenju sa JSON formatom |
| **QoS** | Quality of Service | Nivoi garancije isporuke poruka u MQTT protokolu (`QoS 0`, `QoS 1`, `QoS 2`) |
| **SCADA** | Supervisory Control and Data Acquisition | Industrijska operaterska konzola za nadzor telemetrije mreže i upravljanje dispečingom u realnom vremenu |
| **SoC** | State of Charge | Raspoloživi energetski kapacitet baterijske banke izražen u procentima ($0\% - 100\%$) |
| **TTL** | Time-To-Live | Vremenski period važenja privremenih operativnih ključeva uskladištenih u Redis memoriji |

\newpage