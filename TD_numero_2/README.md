---
# Exercices à Rendre

## 1.1) Questions du Cours nº1

Soit l'exemple d'interblockage du premier cours :

```
MPI_Comm_rank(comm, &myRank);

if(myRank == 0){
    MPI_Ssend(sendbuf1, count, MPI_INT, 2, tag, comm);
    MPI_Recv(recvbuf1, count, MPI_INT, 2, tag, comm, &status);
}
else if(myRank == 1){
    MPI_Ssend(sendbuf2, count, MPI_INT, 2, tag, comm);
}
else if(myRank == 2){
    MPI_Recv(recvbuf1, count, MPI_INT, MPI_ANY_SOURCE, tag, comm, &status);
    MPI_Ssend(sendbuf2, count, MPI_INT, 0, tag, comm);
    MPI_Recv(recvbuf2, count, MPI_INT, MPI_ANY_SOURCE, tag, comm, &status);
}
```

L'interblockage arrive quand les processus attendent des données mutuellement.


### Un premier scénario où il n'y a pas d'interblocage 

L'ordre de rank 0-1-2 ne pose pas un problème d'interblockage indefinit. Dans ce cas, le processus 0 envoie le message vers le processus 2 et es mis en attente. Le même se passe avec le processus 1 ensuite. Enfin, le processus 2 reçoit le message du processus 0, qui est alors prêt à recevoir le message du processus. 

### Un deuxième scénario où il y a interblocage

L'ordre de rank 1-2-0 pose un problème d'interblockage indéfinit. Dans ce cas, le processus 1 envoie un message vers le processus 2, qui le reçoit tout de suite. Ensuite, le processus 2 envoie un message vers le processus 1 et est mis en attente. Enfin, le processus 1 envoie un message vers le processus deux et est mis en attente aussi. 

On peut analyser les six possibilités de permutation entre et on voit que trois parmi eux posent des problèmes. Si on considère ces scénarios équiprobables, la probabilité d'avoir un interblockage est de 50%.

---

## 1.2) Questions du Cours nº2

On sait bien que, selon la Loi d'Amdhal on peut obtenir une accélération maximale de *1/f*, où *f* est la partie du processus qui n'est pas parallélisée. Ainsi, étant donnée *f = 10%*, on aurait l'accélération maximale :

$$ S = \frac{1}{f} = 10 $$

Pour ce jeu de données, si on choisit 4 noeuds de calcul, on pourrait obtenir une accélération d'environ 300%, ce qui semble assez raisonnable en tant que compromis entre la quantité de centres de calcul et l'accélération obtenue.

Selon la Loi d'Amdhal, pour obtenir une accélération de 4 fois, il faut avoir *n = 6*. Ainsi, selon la Loi de Gustafson : 

$$ S(n) = \frac{t_s+nt_p}{t_s+t_p} \Rightarrow S(4) = \frac{t_s+6t_p}{t_s+t_p} $$

On en obtient *tₛ = 0,4* et *tₚ = 0,6*. Ainsi, pour trouver le nouveau speedup avec le double de données :

$$ S' = \frac{S}{2t_p + t_s} = 2,5 $$

L'accélération maximale qu'Alice peut espérer, dans ce cas, est de 250%.

---

## 1.3) Ensemble de Mandelbrot

### 1) Répartition Équitable

Le code se trouve dans le ficher *mandelbrot.py*. Les temps d'exécution trouvés sont : 

| Nombre de processus 	| Temps (s) 	|
|:---:	|:---:	|
| 1 	| 3,25 	|
| 2 	| 1,90 	|
| 3 	| 1,58 	|
| 4 	| 1,42 	|

On peut alors manipuler la Loi d'Amdhal pour estimer la fraction du code qui est effectivement parallélisée :

$$  S = \frac{n}{1+(n-1)f} \Rightarrow  f = \frac{n-s}{s(n-1)}  $$

On trouve donc une fraction d'environ *f = 21,67%*.

### 2) Topologie Maître-esclave

Le code se trouve dans le fichier *mandelbrot_master_slave.py*. Les temps d'exécution trouvés sont : 

| Nombre de processus 	| Temps (s) 	|
|:---:	|:---:	|
| 1 	|  -    |
| 2 	| 3,39  |
| 3 	| 2,19  |
| 4 	| 1,75  |

On en conclure que la topologie maître-esclave est moins efficace dans ce cas car le processus maître ne fait pas le calcul de Mandelbrot, et ses ressources sont alors sous-utilisées vu que le contrôl est léger en ressources.

---

## 1.4) Produit Matrice-Vecteur

### 1) Vecteur par colonne

Le code se trouve dans le fichier *matvec_column.py*.

### 2) Vecteur par ligne

Le code se trouve dans le fichier *matvec_ligne.py*.

---