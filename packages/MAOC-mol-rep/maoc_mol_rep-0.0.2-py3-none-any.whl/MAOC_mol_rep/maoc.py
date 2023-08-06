#!/usr/bin/env python
# coding: utf-8

# In[1]:


def sigma_lambda_opt(data=None,target=None,split=2,kernel='Laplacian',min_sigma=1,step=1000,max_sigma=20000,shuffle=True):
    lambd   = np.array([1e-10, 1e-08, 1e-05, 1e-03, 1e+00])
    ert_mae=[]
    ert_nr=[]
    for t in lambd:
        Z=pd.concat([pd.DataFrame(data),pd.DataFrame(target)],axis=1)
        kf = KFold(n_splits=split, shuffle=shuffle,random_state=137)
        kf.get_n_splits(Z)
        tab=[]
        for train_index, test_index in kf.split(Z):
            mae=[]
            nr=[]
            X_train = Z.iloc[train_index].drop(list(Z.iloc[train_index].iloc[:,-1:]),axis=1)
            X_test = Z.iloc[test_index].drop(list(Z.iloc[train_index].iloc[:,-1:]),axis=1)
            y_train = Z.iloc[train_index].iloc[:,-1:][list(Z.iloc[train_index].iloc[:,-1:])[0]]
            y_test = Z.iloc[test_index].iloc[:,-1:][list(Z.iloc[test_index].iloc[:,-1:])[0]]
            for i in range(min_sigma,max_sigma,step):
                if kernel == 'Laplacian':
                    K=laplacian_kernel(X_train,X_train,i)
                    K[np.diag_indices_from(K)] +=t
                    v=np.mean(np.abs(np.dot(laplacian_kernel(X_test,X_train,i),cho_solve(K,y_train))-y_test))
                else:
                    K=gaussian_kernel(X_train,X_train,i)
                    K[np.diag_indices_from(K)] +=t
                    v=np.mean(np.abs(np.dot(gaussian_kernel(X_test,X_train,i),cho_solve(K,y_train))-y_test))
                mae.append(v)
                nr.append(i)
            A=pd.DataFrame(mae,columns=['mae'])
            B=pd.DataFrame(nr,columns=['Nr'])
            C=pd.concat([A,B],axis=1)
            tab.append(C)
        ert_mae.append((sum(tab)/len(tab)).loc[(sum(tab)/len(tab))['mae'] == (sum(tab)/len(tab))['mae'].min()]['mae'])
        ert_nr.append((sum(tab)/len(tab)).loc[(sum(tab)/len(tab))['mae'] == (sum(tab)/len(tab))['mae'].min()]['Nr'])
        D=pd.concat([pd.DataFrame(np.array(ert_mae),columns=['A']),pd.DataFrame(np.array(ert_nr),columns=['B']),pd.DataFrame(np.array(lambd),columns=['C'])],axis=1)
        opt_sig=float(D.loc[D['A'] == D['A'].min()]['B'])
        opt_lambda=float(D.loc[D['A'] == D['A'].min()]['C'])
    return(opt_sig,opt_lambda)


# In[2]:


def KRR(target=None,input_data=None,kernel='Laplacian',step=200,test_size=0.2,sigma=1,lambd=1e-5):  
    MAE=[]
    std_A=[]
    std_B=[]
    std_D=[]
    R2=[]
    nr=[]
    RMSE=[]
    prop=target
    data=input_data
    sigma=sigma
    for i in range(100,int(float(input_data.shape[0])*(1.0-test_size)),step):
        mae=[]
        r2=[]
        rmse=[]
        for s in range(0,6,1):
            X,x,Y,y=train_test_split(data,prop,test_size=test_size,random_state=137,shuffle=True)
            if kernel == 'Laplacian':
                K=laplacian_kernel(X[:i],X[:i],sigma)
                K[np.diag_indices_from(K)] +=lambd
                v=np.mean(np.abs(np.dot(laplacian_kernel(x,X[:i],sigma),cho_solve(K,Y[:i]))-y))
            else :
                K=gaussian_kernel(X[:i],X[:i],sigma)
                K[np.diag_indices_from(K)] +=lambd
                v=np.mean(np.abs(np.dot(gaussian_kernel(x,X[:i],sigma),cho_solve(K,Y[:i]))-y))
            mae.append(v)
            r2.append(r2_score(y,y_pred))
            rmse.append(mean_squared_error(y, y_pred, squared=False))
        MAE.append(np.mean(mae))
        R2.append(np.mean(r2))
        RMSE.append(np.mean(rmse))
        nr.append(i)
        std_A.append(np.std(mae))
        std_B.append(np.std(r2))
        std_D.append(np.std(rmse))
    A=pd.DataFrame(MAE,columns=['mae'])
    B=pd.DataFrame(R2,columns=['r2'])
    D=pd.DataFrame(RMSE,columns=['rmse'])
    T=pd.DataFrame(nr,columns=['Nr'])
    stdA=pd.DataFrame(std_A,columns=['std_MAE'])
    stdB=pd.DataFrame(std_B,columns=['std_R^2'])
    stdD=pd.DataFrame(std_D,columns=['std_RMSE'])
    C=pd.concat([T,A,stdA,B,stdB,D,stdD],axis=1)
    return C


# In[3]:


def PCX_MAOC(path=None, basis_set='pcseg-0',charge=0,spin=0,nr_pca=1):
    from pyscf import scf,gto,lo
    import glob
    import numpy as np
    from sklearn.decomposition import PCA
    import pandas as pd
    from natsort import natsorted
    atom=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe']
    z=[x for x in range(1,55,1)]
    Atom=pd.DataFrame(atom,columns=['Atom'])
    Z=pd.DataFrame(z,columns=['Z'])
    tab=pd.concat([Atom,Z],axis=1)
    rep_stored=[]
    for file in natsorted(glob.glob(path)):
        q=pd.DataFrame([x.split() for x in open(file).readlines()[2:]])[0]
        atom_types=[x for x in pd.DataFrame(q)[0] if x is not None]
        atom_charge=[]
        for g in atom_types:
            atom_charge.append(tab['Z'][tab.index[tab['Atom'] == g].tolist()[0]])
        mol1 = gto.Mole()
        mol1.atom = file
        mol1.charge=charge
        mol1.spin=abs((mol1.nelectron) % 2)
        p=list(set(atom_charge))
        atom_1=[]
        for t in list(p):
            atom_1.append(tab['Atom'][tab.index[tab['Z'] == t].tolist()[0]])
        atom_1=[x for x in atom_1 if x is not None]
        times=atom_charge.count(max(atom_charge))
        typ=tab['Atom'][tab.index[tab['Z'] == max(atom_charge)].tolist()[0]]
        dic={x:basis_set for x in atom_1}
        dic[str(typ)]=gto.basis.load(basis_set, tab['Atom'][tab.index[tab['Z'] == (max(atom_charge)-mol1.charge)].tolist()[0]])
        atom_types=[]
        mol1.basis=dic
        mol1.build()
        core=lo.orth_ao(mol1)
        core=pd.DataFrame(core)
        for col in core:
            core[col] = core[col].sort_values(ignore_index=True,ascending=False)
        sqr_core = core.sort_values(by =0, axis=1,ascending=False)
        sqr_core=abs(pd.DataFrame(sqr_core)).round(4)
        pca = PCA(n_components=nr_pca)
        rep_stored.append(np.array(pca.fit_transform(sqr_core)).T.flatten())
    return rep_stored


# In[4]:


def Full_MAOC(path=None, basis_set='pcseg-0',charge=0,spin=0):
    from pyscf import scf,gto,lo
    import glob
    import numpy as np
    import pandas as pd
    from natsort import natsorted
    atom=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe']
    z=[x for x in range(1,55,1)]
    Atom=pd.DataFrame(atom,columns=['Atom'])
    Z=pd.DataFrame(z,columns=['Z'])
    tab=pd.concat([Atom,Z],axis=1)
    rep_stored=[]
    for file in natsorted(glob.glob(path)):
        q=pd.DataFrame([x.split() for x in open(file).readlines()[2:]])[0]
        atom_types=[x for x in pd.DataFrame(q)[0] if x is not None]
        atom_charge=[]
        for g in atom_types:
            atom_charge.append(tab['Z'][tab.index[tab['Atom'] == g].tolist()[0]])
        mol1 = gto.Mole()
        mol1.atom = file
        mol1.charge=charge
        mol1.spin=abs((mol1.nelectron) % 2)
        p=list(set(atom_charge))
        atom_1=[]
        for t in list(p):
            atom_1.append(tab['Atom'][tab.index[tab['Z'] == t].tolist()[0]])
        atom_1=[x for x in atom_1 if x is not None]
        times=atom_charge.count(max(atom_charge))
        typ=tab['Atom'][tab.index[tab['Z'] == max(atom_charge)].tolist()[0]]
        dic={x:basis_set for x in atom_1}
        dic[str(typ)]=gto.basis.load(basis_set, tab['Atom'][tab.index[tab['Z'] == (max(atom_charge)-mol1.charge)].tolist()[0]])
        atom_types=[]
        mol1.basis=dic
        mol1.build()
        core=lo.orth_ao(mol1)
        core=pd.DataFrame(core)
        for col in core:
            core[col] = core[col].sort_values(ignore_index=True,ascending=False)
        sqr_core = core.sort_values(by =0, axis=1,ascending=False)
        sqr_core=abs(pd.DataFrame(sqr_core)).round(4)
        rep_stored.append(sqr_core.to_numpy().flatten())
    return rep_stored





