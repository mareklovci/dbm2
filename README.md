# KIV/DBM2

## Statistické zpracování dat o léčbě mozkových příhod

### Současný stav

Anonymizovaný dataset o výsledcích léčby pacientů s mozkovou příhodou ve FN Plzeň za 2016-2017. U pacientů je mimo jiné identifikován etiologický typ mozkové mrtvice, klinický výsledek (škála mRS), míra vstupního deficitu (škála NIHSS), přítomnost rizikových faktorů. Data nejsou úplná, často jsou některé hodnoty neznámé. 

### Úkol
1. Zhodnoťte závislosti dobrého klinického výsledku (mRS-out: hodnota 1 oproti 0), případně mortalitu (mRS – 1Y: hodnota 6 oproti 0-5) jednorozměrnou regresí na: 
    1. věku
    2. pohlaví
    3. vstupního NIHSS (TSS příjem)
    4. rozdílu výstupní-vstupní NIHSS
    
2. Vytvořte Kaplan–Meierovu křivku přežití pro jednotlivé stanovené diagnózy a podrobně popište proces vytvoření a její vlastnosti.   
      
Pozn.: 
Hodnota mRS-out = 7 je u chybějících dat, tyto pacienty je nutno z analýzy vyloučit, případně zpětně podle výsledků analýzy do diskuse porovnat strukturu těchto pacientů se strukturou hodnoceného souboru.
Je otázka, jak se postavit k problému MRS Před s hodnotou 3, kdy už byl vstupní stav "nedobrý".

## Python

```shell script
$ pip freeze > requirements.txt
```
