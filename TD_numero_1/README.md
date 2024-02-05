
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`





## lscpu

```
CPU(s):                  8
  On-line CPU(s) list:   0-7
Vendor ID:               GenuineIntel
  Model name:            11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80GHz
    CPU family:          6
    Model:               140
    Thread(s) per core:  2
    Core(s) per socket:  4
Caches (sum of all):
  L1d:                   192 KiB (4 instances)
  L1i:                   128 KiB (4 instances)
  L2:                    5 MiB (4 instances)
  L3:                    12 MiB (1 instance)
```

<!-- *Des infos utiles s'y trouvent : nb core, taille de cache* -->



## Produit matrice-matrice

### Variation de la taille des matrices

  taille          | time    | MFlops  
------------------|---------|---------
1023              | 1,20830 | 1772             
1024              | 2,60682 | 828  
1025              | 1,21307 | 1775

<!-- EXPLIQUER -->

### Permutation des boucles

<!-- *Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :* -->

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  
------------------|---------|---------
i,j,k (origine)   | 1,42015 | 1521      
j,i,k             | 2,06684 | 1096     
i,k,j             | 2,83176 | 757      
k,i,j             | 3,31695 | 662
j,k,i             | 0,55592 | 3854
k,j,i             | 0,56492 | 3790


<!-- *Discussion des résultats* -->

### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops(n=1024)  | MFlops(n=2048) | MFlops(n=512)
------------------|---------|----------------|---------------
1                 | 791     | 313            | 814           
2                 | 825     | 273            | 713            
3                 | 627     | 291            | 750
4                 | 504     | 257            | 570
5                 | 429     | 300            | 797
6                 | 584     | 289            | 855
7                 | 711     | 273            | 853
8                 | 643     | 301            | 760

<!-- EXPLICAR -->


### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  | 
1024              |  |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
