# Matrix of Orthogonalised Atomic Orbital Coefficients Representation for Radicals and Ions

The code provided by this package is used to generate the MAOC representation, which was first introduced in the article "Matrix of Orthogonalised Atomic Orbital Coefficients Representation for Radicals and Ions" by authors Stiv Llenga and Ganna Gryn'ova. 
Because the size of the MAOC representation is quite large and proportional to the number of atoms and the basis set used to generate it, a new version of MAOC known as PCX-MAOC is created, and the code to generate it is also included in this package. Since the purpose of this package is to provide the code to reproduce the results shown in the article, the code used to optimise the KRR hyperparameters (sigma and lambda) together with the KRR model employed is included. 

If you have any questions about how to use the code, please send an email to stiv.llenga@h-its.org or call this number (from 09:00-19:00 CET): +49 (0)6221 – 533 – 326.

Because there are only four functions in this package, we will go through them all to better understand the input and what users should expect as output. 

Before anything else, users must install/import a few other packages in order to use the code provided by this one. The names of these packages, as well as their versions and locations, are listed below:

| Dependencies | Version | PATH |
| --- | --- | --- |
| `pandas` | 1.0.5  | https://pandas.pydata.org/ | 
| `numpy`  | 1.20.0 | https://numpy.org/ |
| `scikit-learn` | 1.2.1 | https://scikit-learn.org/stable/ | 
| `pyscf` | 2.1 | https://pyscf.org/index.html | 
| `qml` | 0.4.0.27 | https://www.qmlcode.org/index.html | 
| `natsort` | 8.3.1 | https://natsort.readthedocs.io/en/stable/index.html |
   
In addition to the packages listed, we recommend using this package for zero padding of numpy arrays to equal the size of two arrays or make arrays of an ndarray of the same size: 

| `master-strange-mol-rep` | 0.0.1 | https://pypi.org/project/master-strange-mol-rep/ |

If you encounter an error, please ensure that the dependencies are imported correctly, as shown below:

import pandas as pd
import numpy as np
import glob
import sys
from sklearn.decomposition import PCA
from pyscf import scf,gto,lo
from qml.math import cho_solve
from qml.kernels import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from natsort import natsorted
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from master_strange_mol_rep import mol_rep

## a) Generating the MAOC representation  :

MAOC representation is a new quantum-inspired representation that takes the charge and spin multiplicity of the studied systems into account. The authors made sure that the algorithm that generates MAOC was written in such a way that anyone could use it as a black box. 
Since MAOC is new and many questions may arise regarding how, where, and why to use it to represent molecular systems, a tutorial providing examples of how to use some MAOC characteristics is shown in our github (https://github.com/HITS-CCC).

The Full_MAOC function, which generates the full MAOC representation, is constructed as follows: 
   
####   output=Full_MAOC(path=None, basis_set='pcseg-0',charge=0,spin=0)
   
   INPUT:
   
   * --path       -> (Str) The full path to your xyz files. Keep in mind that the *.xyz extension is required ;
   
   * --basis_set   -> (Str) The basis set that the user wishes to use to generate orthogonalized atomic orbitals. The reference basis set is kept unchanged (ANO), but users can simply modify the code to change it (defailt: 'pcseg-0') ;
   
   * --charge -> (Int) The molecular system's charge (default:0) ;
   
   * --spin -> (Int) The molecular system's spin multiplicity (default:0).
   
   OUTPUT:
   
   * output -> The MAOC ndarray sorted and flattened to ensure that it meets all of the symetry requirements for being a rotationally, permutationally, and translationally invariant representation.
  
Comments:
   
Keep in mind that the shape of MAOC is linked to the basis set used to generate it. Please read the article and the supporting information for some tips on selecting the basis set that will make your experience with MAOC more enjoyable and improve the accuracy of your ML models. 

## b) Generating the PCX-MAOC representation :

MAOC representation can be a one-of-a-kind representation because it constructs the compound space using orbital information, but the main issue is that it is dependent on the size of the system and the basis set used to generate it.
For large compounds, such as graphenoids or some compounds in the REDOX dataset, generating MAOC can be a painful process in which users must wait a few seconds to minutes for the representation to be generated and the ability of the majority of personal computers to perform operations on the generated representation is limited. 
The size of the MAOC for large systems is related not only to the time and space required to generate and store the representation, but also to the ease with which this representation can be used for machine learning. This is why the authors of the article introduce the PCX-MAOC, which is much more compact, suitable for ML applications, and produced better results than even the Full MAOC for a number of ML tasks.

The PCX_MAOC function, which generates the PCX MAOC representation, is constructed as follows:
   
####   output=PCX_MAOC(path=None, basis_set='pcseg-0',charge=0,spin=0,nr_pca=1)
   
   INPUT:
   
   * --path       -> (Str) The full path to your xyz files. Keep in mind that the *.xyz extension is required ;
   
   * --basis_set   -> (Str) The basis set that the user wishes to use to generate orthogonalized atomic orbitals. The reference basis set is kept unchanged (ANO), but users can simply modify the code to change it (default: 'pcseg-0') ;
   
   * --charge -> (Int) The molecular system's charge (default:0);
   
   * --spin -> (Int) The molecular system's spin multiplicity (default:0) ;
   
   * --nr_pca -> (Int) The number of principal components used in the representations generated by using the PCA dimensionality reduction technique to reduce the sorted matrix of atomic orbital coefficients (default:1) .
   
   OUTPUT:
   
   * output -> The PCX MAOC ndarray sorted and flattened to ensure that it meets all of the symetry requirements for being a rotationally, permutationally, and translationally invariant representation.
   
   Comments:
   
Please refer to the SI of the article this project introduces for the number of principal components that produces the best machine learning performance. 


## c) Sigma and lambda KRR hyperparameter optimization  :

The code for the optimization of the KRR hyperparameters is provided, allowing readers to reproduce the results in the article. The code is a more-or-less direct implementation of the code found in the qml package. The optimization algorithm compares different sigmas (changeable) and lambdas combinations (1e-10, 1e-08, 1e-05, 1e-03, 1e0) to find the best option. 

   Command:
   
####   opt_sigma,opt_lambda=sigma_lambda_opt(data=None,target=None,split=2,kernel='Laplacian',min_sigma=1,step=1000,max_sigma=20000,shuffle=True)
   
   INPUT:
   
   * --data -> (Str) The dataframe or ndarray of the molecular representations ;
   
   * --target -> (Str) The property under investigation ;
    
   * --split -> (Int) The CV used for hyperparameter optimization (default:2) ;
   
   * --kernel -> (Str) The kernel type, laplacian or gaussian (default:'Laplacian') ;
   
   * --min_sigma -> (Int) The smallest sigma value (default:1) ;
   
   * --step -> (Int) The step of the optimization grid (default:1000) ;
   
   * --max_sigma -> (Int) The biggest sigma value (default:20000) ;
   
   * --shuffle -> (Bol) Allow data shuffling (default:True) .
   
   OUTPUT:
   
   * opt_sigma -> The sigma hyperparameter value that, when combined with the best lambda value, yields the best ML results for a given representation and ML task.
   
   * opt_lambda -> The lambda hyperparameter value that, when combined with the best sigma value, yields the best ML results for a given representation and ML task. 
   
   Comments:
   
In this grid search, only lambda values are fixed. Please feel free to modify the code to meet your specific needs and desires. 
   
## d) Kernel Ridge Regression :

The learning curves generated in the article can be reproduced using this function. Users who intend to use it for their own research should keep in mind that the code employs a 5-fold CV that is not changeable. Users can easily change this fact by manipulating the code. The code is a more-or-less direct implementation of the code found in the qml package.

   Command:
   
####   output=KRR(target=None,input_data=None,kernel='Laplacian',step=200,test_size=0.2,sigma=1,lambd=1e-05)
   
   INPUT:
   
   * --target      -> (Str) The property under investigation ;
   
   * --input_data -> (Str) The dataframe or ndarray of the molecular representations ;
   
   * --kernel    -> (Str) The kernel type, laplacian or gaussian (default:'Laplacian') ;
   
   * --step      -> (Int) The number of structures introduced into the training set size per turn (default: 200) ;
   
   * --test_size      -> (Int) The test ratio (default:0.2) ;
   
   * --sigma      -> (Int) Sigma's optimised value (default:1) ;
   
   * --lambd      -> (Int) Sigma's optimised value (default:1e-05) .
   
   OUTPUT:
   
   * output -> The learning curve table in Pandas .
   
   Comments:
   
The previous code can be linked to this one to ensure workflow automation. 
