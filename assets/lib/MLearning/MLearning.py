from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from matplotlib.colors import ListedColormap
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
from sklearn.svm import SVC
import scipy.io as sio
import pandas as pd
import numpy as np
import os,sys



sys.path.append('assets/lib/Signal')
import Signal as sg

import warnings
warnings.filterwarnings("ignore")


class PRD2ML(object):
    def __init__(self,*args):
        self.__kernel = ['make_moons','make_circles','linearly_separable']
        self.__protocol = ['TaBa','TaBa_low','TaBa_high']
        self.__Nepoch_count = 0
        self.__clf = []

    def Setfs(self,fs,*args):
        self.__sig = sg.sigTools(fs,del_band=['Gamma'])
        self.__RT_data = [np.linspace(0, 10, int(1/(1/240)))*0 for i in range(8)]

    def SetDataset(self,Dataset=True,*args):
        if Dataset:
            self.__loadDatabase()
        else:
            self.__Dataset = Dataset       

    def __readDataset(self,root,pos,label,*args):
        mat = sio.loadmat('ADHD_61P/'+root)
        data = [mat[label][i][pos] for i in range(len(mat[label]))]
        del mat
        return data

    def __loadDatabase(self,*args):
        content,self.__Dataset = os.listdir('ADHD_61P'),[]
        for root in content:
            CHN = [np.array(self.__readDataset(root,i,root.split('.')[0])) for i in range(8)]
            self.__Dataset.append(CHN)
        del CHN

    def __getData_Epoch(self,spc_data,n,*args):
        if self.__Nepoch_count < n+19: pass
        else:
            self.__Nepoch_count = 0

    def __ChExtract(self,CHN,coh_pattern=None,RT=False,*args):
        CHN_fil,PWELCH,CorrDim,TaBaRatio,TaBaRatio_low,TaBaRatio_high = [],[],[],[],[],[]
        if RT: CHN = self.__RT_data
        
        ### Apply filters ###
        for chn in CHN: CHN_fil.append(self.__sig.filfit.apply(chn,Notch=False))

        ### Get it power ###
        for chn in CHN_fil:
            aux = []
            for fil in chn: f,p = self.__sig.Pwelch(fil); aux.append([f,p])
            PWELCH.append(aux)

        PWELCH = np.array(PWELCH)

        ### Get it Correlation Dimention ###
        for chn in CHN: CorrDim.append(self.__sig.corrDim(chn))
        
        ### Get it Theta/Beta ratio ###
        for chn in PWELCH: TaBaRatio.append(self.__sig.TaBaRatio(chn[1][1]/np.linalg.norm(chn[1][1]),chn[3][1]/np.linalg.norm(chn[3][1]),mean=True))
                                            
        ### Get it Theta/Beta_low ratio ###
        for chn in PWELCH: TaBaRatio_low.append(self.__sig.TaBaRatio(chn[1][1]/np.linalg.norm(chn[1][1]),chn[4][1]/np.linalg.norm(chn[4][1]),mean=True))

        ### Get it Theta/Beta_high ratio ###
        for chn in PWELCH: TaBaRatio_high.append(self.__sig.TaBaRatio(chn[1][1]/np.linalg.norm(chn[1][1]),chn[5][1]/np.linalg.norm(chn[5][1]),mean=True))

        TaBaRatio,TaBaRatio_low,TaBaRatio_high = np.mean(np.array(TaBaRatio)),np.mean(np.array(TaBaRatio_low)),np.mean(np.array(TaBaRatio_high))
        CHN_fil,PWELCH,CorrDim = np.array(CHN_fil),np.array(PWELCH),np.mean(np.array(CorrDim))
                
        return CHN_fil,PWELCH,CorrDim,TaBaRatio,TaBaRatio_low,TaBaRatio_high

    def __RT_Data(self,dot,*args):
        
        for i in range(len(dot)): self.__RT_data[i] = np.append(self.__RT_data[i][1:], [dot[i]])

    def RT_ML(self,CHNs,CHN_sel=0,*args):
        self.__RT_Data(CHNs)
        ################### Preprocess #####################
        if CHN_sel == 'mean':
            for i in range(len(CHNs)): pass
        else:
            _,PSDW,_,_,_,_= self.__ChExtract(None,RT=True)
            T_index = np.mean(np.array(PSDW[CHN_sel][1][1]))
            B_index = np.mean(np.array(PSDW[CHN_sel][3][1]))
            B_low_index = np.mean(np.array(PSDW[CHN_sel][4][1]))
            B_high_index = np.mean(np.array(PSDW[CHN_sel][5][1]))
        ######################## ML #########################
        return PSDW,T_index,B_index,B_low_index,B_high_index
        

    def __dataFix2Clf(self,*args):
        Corr,TaBa,TaBa_low,TaBa_high = [],[],[],[]
        X_data_M1,X_data_M2,X_data_M3 = [],[],[]
        
        for i in range(len(self.__Dataset)):
            _,_,D1,D2,D3,D4 =  self.__ChExtract(self.__Dataset[i])
            Corr.append(D1)
            TaBa.append(D2)
            TaBa_low.append(D3)
            TaBa_high.append(D4)

        del D1,D2,D3,D4
        
        for i in range(len(Corr)):
            X_data_M1.append([TaBa[i],Corr[i]])
            X_data_M2.append([TaBa_low[i],Corr[i]])
            X_data_M3.append([TaBa_high[i],Corr[i]])

        return [np.array(X_data_M1),np.array(X_data_M2),np.array(X_data_M3)]

    def Train(self,protocol,auto_plot=False,*args):
        D = self.__dataFix2Clf()
        X = D[self.__protocol.index(protocol)]

        h = 0.02  # step size in the mesh

        names = [
            "Nearest Neighbors",
            "Linear SVM",
            "RBF SVM",
            "Gaussian Process",
            "Decision Tree",
            "Random Forest",
            "Neural Net",
            "AdaBoost",
            "Naive Bayes",
            "QDA",
        ]

        self.__clf = [None for n in names]
        appd,appd_aux = self.__clf,[]

        classifiers = [
            KNeighborsClassifier(3),
            SVC(kernel="linear", C=0.025),
            SVC(gamma=2, C=1),
            GaussianProcessClassifier(1.0 * RBF(1.0)),
            DecisionTreeClassifier(max_depth=5),
            RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
            MLPClassifier(alpha=1, max_iter=1000),
            AdaBoostClassifier(),
            GaussianNB(),
            QuadraticDiscriminantAnalysis(),
        ]

        _, y = make_classification(
            n_features=2, n_redundant=0, n_informative=2, random_state=1, n_clusters_per_class=1
        )

        y = y[:len(X)]


        rng = np.random.RandomState(2)
        X += 2 * rng.uniform(size=X.shape)
        linearly_separable = (X, y)

        datasets = [
            make_moons(noise=0.3, random_state=0),
            make_circles(noise=0.2, factor=0.5, random_state=1),
            linearly_separable,
        ]

        figure = plt.figure(figsize=(27, 9))
        i = 1
        
        # iterate over datasets
        for ds_cnt, ds in enumerate(datasets):
            # preprocess dataset, split into training and test part
            X, y = ds
            X = StandardScaler().fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.4, random_state=42
            )

            x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
            y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
            xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

            if auto_plot:
                # just plot the dataset first
                cm = plt.cm.RdBu
                cm_bright = ListedColormap(["#FF0000", "#0000FF"])
                ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
                if ds_cnt == 0:
                    ax.set_title("Input data")
                # Plot the training points
                ax.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors="k")
                # Plot the testing points
                ax.scatter(
                    X_test[:, 0], X_test[:, 1], c=y_test, cmap=cm_bright, alpha=0.6, edgecolors="k"
                )
                ax.set_xlim(xx.min(), xx.max())
                ax.set_ylim(yy.min(), yy.max())
                ax.set_xticks(())
                ax.set_yticks(())
            i += 1

            # iterate over classifiers
            for name, clf in zip(names, classifiers):
                if auto_plot:
                    ax = plt.subplot(len(datasets), len(classifiers) + 1, i)
                clf.fit(X_train, y_train)
                appd[names.index(name)] = clf
                score = clf.score(X_test, y_test)

                if auto_plot:
                    # Plot the decision boundary. For that, we will assign a color to each
                    # point in the mesh [x_min, x_max]x[y_min, y_max].
                    if hasattr(clf, "decision_function"):
                        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
                    else:
                        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
                        print(Z)

                    # Put the result into a color plot
                    Z = Z.reshape(xx.shape)
                    ax.contourf(xx, yy, Z, cmap=cm, alpha=0.8)

                    # Plot the training points
                    ax.scatter(
                        X_train[:, 0], X_train[:, 1], c=y_train, cmap=cm_bright, edgecolors="k"
                    )
                    # Plot the testing points
                    ax.scatter(
                        X_test[:, 0],
                        X_test[:, 1],
                        c=y_test,
                        cmap=cm_bright,
                        edgecolors="g",
                        alpha=0.6,
                    )

                    ax.set_xlim(xx.min(), xx.max())
                    ax.set_ylim(yy.min(), yy.max())
                    ax.set_xticks(())
                    ax.set_yticks(())
                    if ds_cnt == 0:
                        ax.set_title(name)
                    ax.text(
                        xx.max() - 0.3,
                        yy.min() + 0.3,
                        ("%.2f" % score).lstrip("0"),
                        size=15,
                        horizontalalignment="right",
                    )
                    i += 1

            appd_aux.append(appd)

        for i in range(len(appd_aux)): appd_aux[i] = pd.Series(appd_aux[i], index = names) 
        appd_aux = pd.Series(appd_aux, index = self.__kernel)
        self.__clf = appd_aux

        if auto_plot:
            plt.tight_layout()
            plt.show()
        
    def predict(self,kernel,model,*args):
        clf = self.__clf.loc[kernel].loc[model]
        s = clf.predict(np.array([[1,2,4e-8],[2e-5,1e-4,8]]))
        print(s)
    


##ML = PRD2ML()
##ML.Setfs(128)
##ML.SetDataset()
##ML.Train('TaBa_high',auto_plot=False)
##ML.predict('make_moons','RBF SVM')



















































