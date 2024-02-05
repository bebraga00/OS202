# Exercices à Rendre

## Questions du Cours 1

### Un premier scénario où il n'y a pas d'interblocage 

### Un deuxième scénario où il y a interblocage

## 1.2) Questions du Cours nº2

On sait bien que, selon la Loi d'Amdhal on peut obtenir une accélération maximale de 1/f, où f est la partie du processus qui n'est pas parallélisée. Ainsi, étant donnée f = 10%, on aurait l'accélération maximale S = 1/f = 10. Pour ce jeu de données, si on choisit 5 noeuds de calcul, on pourrait obtenir une accélération d'environ 350%, ce qui semble assez raisonnable en tant que compromis entre la quantité de centres de calcul et l'accélération obtenue.

Alors selon la Loi d'Amdhal, pour une accélération de 4 fois, il faut avoir n = 6. Ainsi, selon la Loi de Gustafson, S = (ts + 4tp) / (ts + tp) = (0.1t + 3.6t) / (0.1t + 0.9t) = 3.7t. Finalement : S' = (ts + 8tp) / (ts + 2tp) = 

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

On trouve donc une fraction d'environ $ f = 21,67\% '$.

### 2) Topologie Maître-esclave

Le code se trouve dans le fichier *mandelbrot_master_slave.py*. Les temps d'exécution trouvés sont : 

| Nombre de processus 	| Temps (s) 	|
|:---:	|:---:	|
| 1 	|  -    |
| 2 	| 3,39  |
| 3 	| 2,19  |
| 4 	| 1,75  |

On en conclure que la topologie maître-esclave est moins efficace dans ce cas car le processus maître ne fait pas le calcul de Mandelbrot, et ses ressources sont alors sous-utilisées vu que le contrôl est léger en ressources.


