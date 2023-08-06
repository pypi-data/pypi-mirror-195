import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, roc_curve, auc

class DSTools:
    def __init__(self):
        pass

    @staticmethod
    def roc_optimal_cutoff(y_pred_prob, y_true):
        """
        A function to find the optimal cutoff value for binary classification using Receiver Operating Characteristic (ROC) curve.

        Parameters:
        -----------
        y_pred_prob (array-like): Predicted probabilities for the positive class.

        y_true (array-like): True binary labels.

        Returns:
        -----------
        float: Optimal cutoff value for binary classification.

        Example:
        -----------
        >>> import numpy as np
        >>> from sklearn.metrics import roc_auc_score
        >>> y_pred_prob = np.array([0.2, 0.4, 0.6, 0.8])
        >>> y_true = np.array([0, 0, 1, 1])
        >>> roc_optimal_cutoff(y_pred_prob, y_true)
        0.6
        """
        fpr, tpr, thresholds = roc_curve(y_true=y_true, y_score=y_pred_prob)
        # thresholds are for predicting true (Above which will be predicted as true)
        roc_auc = auc(fpr, tpr)
        optimal_idx = np.argmax(tpr - fpr)
        optimalTrueCutoff = thresholds[optimal_idx]
        sns.lineplot(x=fpr, y=tpr)
        sns.lineplot(x=[0, 1], y=[0, 1], linestyle='dashed')
        sns.scatterplot(x=[fpr[optimal_idx]], y=[tpr[optimal_idx]], s=80, color='green')
        # linestyle takes following input: 'solid', 'dashed', 'dashdot' and 'dotted'
        plt.text(0.5, 0.2, 'AUC: {:.2f}%'.format(roc_auc * 100), fontsize=20)
        plt.text(fpr[optimal_idx] + 0.02, tpr[optimal_idx] - 0.05, 'Optimal Cutoff', fontsize=10)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title('ROC Curve', fontsize=20)
        plt.show()
        return optimalTrueCutoff

    @staticmethod
    def compareRegressors(X, y, regressorList, numOfRun=10, testSize=0.2, regressorNames=None):
        """
        Compares the R2 score of different regressors on a given dataset.

        Parameters:
        -----------
        X : numpy.ndarray or pandas.DataFrame
            The feature matrix of shape (n_samples, n_features).

        y : numpy.ndarray or pandas.Series
            The target vector of shape (n_samples,).

        regressorList : list of regressor objects
            A list of regressors to compare. Each regressor should implement the `fit` and `predict` methods.

        numOfRun : int, optional (default=10)
            The number of times to repeat the train/test split and regression.

        testSize : float, optional (default=0.2)
            The fraction of the data to use as the test set in each run.

        regressorNames : list of strings, optional (default=None)
            A list of names for the regressors. If provided, the names will be used in the plot.

        Returns:
        --------
        None

        Examples:
        ---------
        >>> from sklearn.linear_model import LinearRegression, Ridge, Lasso
        >>> from sklearn.datasets import load_boston
        >>> X, y = load_boston(return_X_y=True)
        >>> regressorList = [LinearRegression(), Ridge(), Lasso(alpha=0.1)]
        >>> compareRegressors(X, y, regressorList, numOfRun=5, testSize=0.3, regressorNames=['LR', 'Ridge', 'Lasso'])
        """
        performanceDataframe = pd.DataFrame()
        modelNumber = 1
        for regressor in regressorList:
            performanceList = []
            n = 1
            while n <= numOfRun:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, random_state=None)
                regressor.fit(X_train, y_train)
                prediction = regressor.predict(X_test)
                r2 = r2_score(y_test, prediction)
                performanceList.append(r2)
                n = n + 1
            modelName = ''
            if regressorNames is not None:
                modelName = regressorNames[modelNumber - 1]
            else:
                modelName = 'Model ' + str(modelNumber)
            performanceDataframe[modelName] = performanceList
            modelNumber = modelNumber + 1
        sns.boxplot(data=performanceDataframe)
        plt.title('Model Performance (R2)', fontsize=15)
        plt.show()

    @staticmethod
    def compareClassifiers(X, y, classifierList, numOfRun=10, testSize=0.2, classifierNames=None):
        """
        Compares the Accuracy score of different classifiers on a given dataset.

        Parameters:
        -----------
        X : numpy.ndarray or pandas.DataFrame
            The feature matrix of shape (n_samples, n_features).
        y : numpy.ndarray or pandas.Series
            The target vector of shape (n_samples,).
        classifierList : list
            A list of scikit-learn classifier objects to evaluate.
        numOfRun : int, optional (default=10)
            The number of times to perform the k-fold cross-validation.
        testSize : float, optional (default=0.2)
            The proportion of the data to include in the test split.
        classifierNames : list, optional (default=None)
            A list of string names for each classifier in classifierList.

        Returns:
        --------
        None

        Examples:
        ---------
        >>> from sklearn.datasets import load_iris
        >>> from sklearn.linear_model import LogisticRegression
        >>> from sklearn.tree import DecisionTreeClassifier
        >>> X, y = load_iris(return_X_y=True)
        >>> classifierList = [LogisticRegression(), DecisionTreeClassifier()]
        >>> compareClassifiers(X, y, classifierList, numOfRun=5, testSize=0.3, regressorNames=['LR', 'DecisionTree'])
        """

        performanceDataframe = pd.DataFrame()
        modelNumber = 1
        for classifier in classifierList:
            performanceList = []
            n = 1
            while n <= numOfRun:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, random_state=None)
                classifier.fit(X_train, y_train)
                prediction = classifier.predict(X_test)
                accuracy = accuracy_score(y_test, prediction)
                performanceList.append(accuracy)
                n = n + 1
            modelName = ''
            if classifierNames is not None:
                modelName = classifierNames[modelNumber - 1]
            else:
                modelName = 'Model ' + str(modelNumber)
            performanceDataframe[modelName] = performanceList
            modelNumber = modelNumber + 1
        sns.boxplot(data=performanceDataframe)
        plt.title('Model Performance (Accuracy)', fontsize=15)
        plt.show()

    @staticmethod
    def showPercentageWithHue(ax, fontsize=8, x_offset=0, y_offset=0):
        """
        Displays the percentage values of on each bar in a bar plot or count plot with hue. The percentages of hues
        in the same group adds up t0 100%

        Parameters:
        -----------
        ax : matplotlib.axes.Axes
            The axes object containing the stacked bar plot.
        fontsize : int, optional (default=8)
            The size of the font used to display the percentage values.
        x_offset : int, optional (default=0)
            The horizontal offset of the percentage values from the left edge of the patches.
        y_offset : int, optional (default=0)
            The vertical offset of the percentage values from the top edge of the patches.

        Returns:
        --------
        None

        Raises:
        -------
        TypeError
            If `ax` is not a matplotlib.axes.Axes object.

        Example:
        --------
        fig, ax = plt.subplots()
        ax.bar(['A', 'B', 'C'], [1, 2, 3], label='Group 1')
        ax.bar(['A', 'B', 'C'], [4, 5, 6], bottom=[1, 2, 3], label='Group 2')
        ax.legend()
        mymodule.showPercentageWithHue(ax)
        plt.show()
        """
        containerList = ax.containers  # When there is hue, ax.containers gives us a list of hue.
        n = 0
        for i in containerList[0].patches:  # containers[0].patches gives us a list composed of hue 0 of each group
            total = i.get_height()
            container = 1
            while container < len(containerList):
                total = total + containerList[container].patches[n].get_height()
                container = container + 1
            container = 0
            while container < len(containerList):
                j = containerList[container].patches[n]
                percentage = '{:.2f}%'.format(100 * j.get_height() / total)
                x_i = j.get_x() + x_offset
                y_i = j.get_y() + j.get_height() + y_offset
                ax.annotate(percentage, (x_i, y_i), size=fontsize)
                container = container + 1
            n = n + 1

    @staticmethod
    def showPercentageWithoutHue(ax, fontsize=8, x_offset=0.0, y_offset=0.0):
        """
        Display the percentage values on top of the bars in a non-hue bar plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The axes object containing the bars to be annotated.
        fontsize : int, optional
            The font size of the percentage labels. Default is 8.
        x_offset : float, optional
            The horizontal offset of the percentage labels from the center of the bars. Default is 0.0.
        y_offset : float, optional
            The vertical offset of the percentage labels from the top of the bars. Default is 0.0.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the axes object does not contain any bars.
        """
        total = 0
        for i in ax.containers[0].patches:
            total = total + i.get_height()
        for i in ax.containers[0].patches:
            percentage = '{:.2f}%'.format(100 * i.get_height() / total)
            x_i = i.get_x() + x_offset
            y_i = i.get_y() + i.get_height() + y_offset
            ax.annotate(percentage, (x_i, y_i), size=fontsize)










