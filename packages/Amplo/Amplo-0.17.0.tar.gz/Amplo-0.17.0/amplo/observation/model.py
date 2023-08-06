#  Copyright (c) 2022 by Amplo.

"""
Observer for checking production readiness of model.

This part of code is strongly inspired by [1].

References
----------
[1] E. Breck, C. Shanging, E. Nielsen, M. Salib, D. Sculley (2017).
The ML test score: A rubric for ML production readiness and technical debt
reduction. 1123-1132. 10.1109/BigData.2017.8258038.
"""

from __future__ import annotations

from copy import deepcopy

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import get_scorer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KernelDensity

from amplo.base import BaseEstimator
from amplo.classification import PartialBoostingClassifier
from amplo.observation._base import BaseObserver, _report_obs
from amplo.regression import PartialBoostingRegressor
from amplo.utils.logging import get_root_logger
from amplo.utils.sys import getsize

__all__ = ["ModelObserver"]

logger = get_root_logger().getChild("ModelObserver")


class ModelObserver(BaseObserver):
    """
    Model observer before putting to production.

    While the field of software engineering has developed a full range of best
    practices for developing reliable software systems, similar best-practices
    for ML model development are still emerging.

    The following tests are included:
        1. TODO: Model specs are reviewed and submitted.
        2. TODO: Offline and online metrics correlate.
        3. TODO: All hyperparameters have been tuned.
        4. TODO: The impact of model staleness is known.
        5. A simpler model is not better.
        6. TODO: Model quality is sufficient on important data slices.
        7. TODO: The model is tested for considerations of inclusion.
    """

    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    _obs_type = "model_observer"

    def observe(
        self,
        model: BaseEstimator,
        data: pd.DataFrame,
        target: str,
        mode: str,
    ) -> list[dict[str, str | bool]]:
        model = deepcopy(model)
        self.check_model_size(model)
        self.check_better_than_linear(model, data, target, mode)
        self.check_noise_invariance(model, data, target, mode)
        self.check_slice_invariance(model, data, target, mode)
        self.check_boosting_overfit(model, data, target, mode)
        return self.observations

    @_report_obs
    def check_model_size(
        self, model: BaseEstimator, threshold=20e6
    ) -> tuple[bool, str]:
        """
        Check the RAM of the model. If it's bigger than 20MB, something is wrong.

        Parameters
        ----------
        threshold : float
            Threshold for latency (in s).

        Returns
        -------
        status_ok : bool
            Observation status. Indicates whether a warning should be raised.
        message : str
            A brief description of the observation and its results.
        """
        logger.info("Checking model size.")
        ram = getsize(model)

        status_ok = ram < threshold
        message = (
            f"A model should occupy more than {threshold // 1e6:.2f}MB of RAM. "
            f"However, the model has a size of {ram // 1e6:.2f}MB."
        )
        return status_ok, message

    @_report_obs
    def check_better_than_linear(
        self, model: BaseEstimator, data: pd.DataFrame, target: str, mode: str
    ) -> tuple[bool, str]:
        """
        Checks whether the model exceeds a linear model.

        This test incorporates the test ``Model 5`` from [1].

        Citation:
            A simpler model is not better: Regularly testing against a very
            simple baseline model, such as a linear model with very few
            features, is an effective strategy both for confirming the
            functionality of the larger pipeline and for helping to assess the
            cost to benefit tradeoffs of more sophisticated techniques.

        Returns
        -------
        status_ok : bool
            Observation status. Indicates whether a warning should be raised.
        message : str
            A brief description of the observation and its results.
        """
        logger.info("Checking whether the model exceeds a linear model.")

        # Make score for linear model
        if mode == self.CLASSIFICATION:
            linear_model = LogisticRegression()
            objective = "neg_log_loss"
        elif mode == self.REGRESSION:
            linear_model = LinearRegression()
            objective = "neg_mean_squared_error"
        else:
            raise AssertionError("Invalid mode detected.")

        # Split data
        y = data[target]
        x = data.drop(target, axis=1)

        # Score
        linear_model_score = np.mean(
            cross_val_score(linear_model, x, y, scoring=objective)
        )
        obs_model_score = np.mean(cross_val_score(model, x, y, scoring=objective))

        # Determine status
        status_ok = obs_model_score > linear_model_score
        message = (
            "Performance of a linear model should not exceed the "
            "performance of the model to observe. "
            f"Score for linear model: {linear_model_score:.4f}. "
            f"Score for observed model: {obs_model_score:.4f}."
        )
        return status_ok, message

    @_report_obs
    def check_noise_invariance(
        self, model: BaseEstimator, data: pd.DataFrame, target: str, mode: str
    ) -> tuple[bool, str]:
        """
        This checks whether the model performance is invariant to noise in the data.

        Noise is injected in a slice of the data. The noise follows
        the distribution of the original data.
        Next, the performance metrics are re-evaluated on this noisy slice.

        Returns
        -------
        status_ok : bool
            Observation status. Indicates whether a warning should be raised.
        message : str
            A brief description of the observation and its results.
        """
        logger.info("Checking model for noise invariance.")

        # Set scorer
        scorer = self.get_scorer_(mode)

        # Train model
        xt, xv, yt, yv = self.get_train_test_(data, target)
        model.fit(xt, yt)

        # Inject noise
        signal_noise_ratio = 5  # This threshold is not super optimized
        xn = deepcopy(xv)
        for key in xv.keys():
            signal_energy = sum(xn[key].values ** 2)
            noise = np.random.normal(0, 1, len(xn))
            noise_energy = sum(noise**2)
            xn[key] = (
                xn[key]
                + np.sqrt(signal_energy / noise_energy * signal_noise_ratio) * noise
            )

        # Arrange message
        status_ok = True
        message = (
            "Model performance deteriorates with realistic noise injection."
            "This indicates too little variance in your data. "
            "Please upload more varied data."
        )

        # Compare performance
        baseline = scorer(model, xv, yv)
        comparison = scorer(model, xn, yv)
        # These thresholds may be optimize
        if comparison / baseline < 0.9 or comparison / baseline > 1.1:
            status_ok = False

        return status_ok, message

    @_report_obs
    def check_slice_invariance(
        self,
        model: BaseEstimator,
        data: pd.DataFrame,
        target: str,
        mode: str,
    ) -> tuple[bool, str]:
        """
        Model performance should be invariant to data slicing.

        Using High Density Regions [1], the weakest slice of 10% data is identified.
        If the optimization metric is significantly (>5%) worse than the average
        metric, a warning is given.

        [1] https://stats.stackexchange.com/questions/148439/what-is-a-highest-density-region-hdr # noqa

        Returns
        -------
        status_ok : bool
            Observation status. Indicates whether a warning should be raised.
        message : str
            A brief description of the observation and its results.
        """
        logger.info("Checking model for slice invariance.")

        # Arrange message
        status_ok = True
        message = (
            "Model performs significantly worse on bad slice of the data. "
            "This indicates too little variance in your data. "
            "Please upload more varied data."
        )

        # Normalize
        y = data[target]
        x = data.drop(target, axis=1)
        x = (x - x.mean()) / x.std()

        # Fit Kernel Density Estimation & get probabilities
        log_probabilities = (
            KernelDensity(kernel="gaussian", bandwidth=1).fit(x).score_samples(x)
        )
        probabilities = np.exp(log_probabilities)

        # Select smallest slice (10%) (selects per class to avoid imbalance)
        if mode == self.CLASSIFICATION:
            slice_indices = []
            for yc in y.unique():
                yc_ind = np.where(y == yc)[0]
                samples = int(np.ceil(len(yc_ind) // 10))  # Ceils (to avoid 0)
                slice_indices.extend(
                    yc_ind[np.argpartition(probabilities[yc_ind], samples)[:samples]]
                )
            objective = "neg_log_loss"
        else:
            slice_indices = np.argpartition(probabilities, int(np.ceil(len(x) // 10)))[
                : int(np.ceil(len(x) // 10))
            ]
            objective = "neg_mean_squared_error"
        scorer = get_scorer(objective)
        train_indices = [i for i in range(len(x)) if i not in slice_indices]
        xt, xv = x.iloc[train_indices], x.iloc[slice_indices]
        yt, yv = y.iloc[train_indices], y.iloc[slice_indices]

        # Train and check performance
        scores = cross_val_score(model, x, y, scoring=objective)
        best_score = np.mean(scores) - np.std(scores)
        model.fit(xt, yt)
        score = scorer(model, xv, yv)
        if score < best_score:
            status_ok = False

        return status_ok, message

    @_report_obs
    def check_boosting_overfit(
        self, model: BaseEstimator, data: pd.DataFrame, target: str, mode: str
    ) -> tuple[bool, str]:
        """
        Checks whether boosting models are overfitted.

        Boosting models are often optimal. Though naturally robust against
        overfitting, it's not impossible to add too many estimators in a
        boosting model, creating complexity to an extent of overfitting.
        This function runs the same model while limiting the estimators, and
        checks if the validation performance decreases.

        Returns
        -------
        status_ok : bool
            Observation status. Indicates whether a warning should be raised.
        message : str
            A brief description of the observation and its results.
        """

        # Check if a boosting model has been selected
        if type(model).__name__ not in [
            *PartialBoostingClassifier._SUPPORTED_MODELS,
            *PartialBoostingRegressor._SUPPORTED_MODELS,
        ]:
            return True, ""

        logger.info("Checking boosting model for overfitting.")

        # Get scorer
        partial_booster: type[PartialBoostingClassifier] | type[
            PartialBoostingRegressor
        ]
        if mode == self.CLASSIFICATION:
            partial_booster = PartialBoostingClassifier
        else:
            partial_booster = PartialBoostingRegressor
        scorer = self.get_scorer_(mode)

        # Split data
        xt, xv, yt, yv = self.get_train_test_(data, target)

        # Fit model
        model.fit(xt, yt)

        # Determine steps & initiate results
        steps = np.ceil(np.linspace(0, partial_booster.n_estimators(model), 7))[1:-1]
        scores = []
        for step in steps:
            # Can directly use scorer, as no training is involved at all
            booster = partial_booster(model, step)
            booster.is_fitted_ = True
            scores.append(scorer(booster, xv, yv))

        # Now, the check fails if there has been a decrease in performance
        status_ok = all(np.diff(scores) / np.max(np.abs(scores)) > 0.001)
        message = (
            "Boosting overfit detected. Please retrain with less estimators. "
            f"Estimators: {steps}, Scores: {scores}"
        )
        return status_ok, message

    @staticmethod
    def get_scorer_(mode: str):
        if mode == "classification":
            objective = "neg_log_loss"
        else:
            objective = "neg_mean_squared_error"
        return get_scorer(objective)

    @staticmethod
    def get_train_test_(
        data: pd.DataFrame, target: str
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        y = data[target]
        x = data.drop(target, axis=1)
        return train_test_split(x, y)
