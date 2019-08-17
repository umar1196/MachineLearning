# Machine Learning
Disease genes prediction using machine learning


## Work flow:

1.Read input file containing Entrez gene id.

2.Download sequences from NCBI for given genes and insert them in locally created database.

3.Retrive sequences from local database.

4.Create sequence similarity matrix using pairwise sequence alignment tool for retrived sequences.

5.Train machine learning model such as linear regression and random forest to predict disease gene.

6.Model evaluation using overall accuracy, preceision and recall. 
