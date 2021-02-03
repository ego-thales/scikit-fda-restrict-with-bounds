"""Feature extraction transformers for dimensionality reduction."""

from typing import List

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted as sklearn_check_is_fitted

from ...._utils import _classifier_fit_distributions
from ....exploratory.depth import Depth, ModifiedBandDepth


class DDGTransformer(BaseEstimator, TransformerMixin):
    r"""Generalized depth-versus-depth (DD) transformer for functional data.

    This transformer takes a list of k depths and performs the following map:

    .. math::
        \mathcal{X} &\rightarrow \mathbb{R}^G \\
        x &\rightarrow \textbf{d} = (D_1^1(x), D_1^2(x),...,D_g^k(x))

    Where :math:`D_i^j(x)` is the depth of the point :math:`x` with respect to
    the data in the :math:`i`-th group using the :math:`j`-th depth of the
    provided list.

    Note that :math:`\mathcal{X}` is possibly multivariate, that is,
    :math:`\mathcal{X} = \mathcal{X}_1 \times ... \times \mathcal{X}_p`.

    Parameters:
        depth_method (default
            :class:`ModifiedBandDepth <skfda.depth.ModifiedBandDepth>`):
            The depth class to use when calculating the depth of a test
            sample in a class. See the documentation of the depths module
            for a list of available depths. By default it is ModifiedBandDepth.
        depth_methods (optional):
            List of depth classes to use when calculating the depth of a test
            sample in a class. See the documentation of the depths module
            for a list of available depths. By default it is None.
            If a list is provided, the parameter depth_method will be ignored.

    Examples:
        Firstly, we will import and split the Berkeley Growth Study dataset

        >>> from skfda.datasets import fetch_growth
        >>> from sklearn.model_selection import train_test_split
        >>> dataset = fetch_growth()
        >>> fd = dataset['data']
        >>> y = dataset['target']
        >>> X_train, X_test, y_train, y_test = train_test_split(
        ...     fd, y, test_size=0.25, stratify=y, random_state=0)

        >>> from skfda.preprocessing.dim_reduction.feature_extraction import \
        ... DDGTransformer
        >>> from sklearn.pipeline import make_pipeline
        >>> from sklearn.neighbors import KNeighborsClassifier

        We classify by first transforming our data using the defined map
        and then using KNN

        >>> pipe = make_pipeline(DDGTransformer(), KNeighborsClassifier())
        >>> pipe.fit(X_train, y_train)
        Pipeline(steps=[('ddgtransformer',
                         DDGTransformer(depth_method=None,
                                        depth_methods=[ModifiedBandDepth()])),
                        ('kneighborsclassifier', KNeighborsClassifier())])

        We can predict the class of new samples

        >>> pipe.predict(X_test)
        array([1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1,
               1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1])

        Finally, we calculate the mean accuracy for the test data

        >>> pipe.score(X_test, y_test)
        0.875

    References:
        Cuesta-Albertos, J. A., Febrero-Bande, M. and Oviedo de la Fuente, M.
        (2017). The DDG-classifier in the functional setting.
        TEST, 26. 119-142.
    """

    def __init__(
        self,
        depth_method: Depth = ModifiedBandDepth(),
        depth_methods: List[Depth] = None,
    ):
        if depth_methods is None:
            self.depth_methods = [depth_method]
        else:
            self.depth_methods = depth_methods

    def fit(self, X, y):
        """Fit the model using X as training data and y as target values.

        Args:
            X (:class:`FDataGrid`): FDataGrid with the training data.
            y (array-like): Target values of shape = (n_samples).

        Returns:
            self (object)
        """
        classes_, distributions_ = _classifier_fit_distributions(
            X, y, self.depth_methods,
        )

        self.classes_ = classes_
        self.distributions_ = distributions_

        return self

    def transform(self, X):
        """Transform the provided data using the defined map.

        Args:
            X (:class:`FDataGrid`): FDataGrid with the test samples.

        Returns:
            X_new (array-like): array of shape (n_samples, G).
        """
        sklearn_check_is_fitted(self)

        return np.transpose([
            distribution.predict(X)
            for distribution in self.distributions_
        ])
