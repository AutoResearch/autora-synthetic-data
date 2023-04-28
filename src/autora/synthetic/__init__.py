"""
Provides an interface for loading and saving synthetic experiments.

Examples:
    >>> from autora.synthetic import retrieve, describe
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt

    The registry is accessed using the `retrieve` function, optionally setting parameters. Here
    we load the Weber-Fechner law:
    >>> s = retrieve("weber_fechner", rng=np.random.default_rng(seed=180))

    Use the describe function to give information about the synthetic experiment:
    >>> describe(s) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    Weber-Fechner Law...

    The synthetic experiement `s` has properties like the name of the experiment:
    >>> s.name
    'Weber-Fechner Law'

    ... a valid metadata description:
    >>> s.metadata  # doctest: +ELLIPSIS
    VariableCollection(...)

    ... a function to generate the full domain of the data (if possible)
    >>> x = s.domain()
    >>> x   # doctest: +ELLIPSIS
    array([[0...]])

    ... the experiment_runner runner which can be called to generate experimental results:
    >>> import numpy as np
    >>> y = s.experiment_runner(x)  # doctest: +ELLIPSIS
    >>> y
    array([[ 0.00433955],
           [ 1.79114625],
           [ 2.39473454],
           ...,
           [ 0.00397802],
           [ 0.01922405],
           [-0.00612883]])

    ... a function to plot the ground truth:
    >>> s.plotter()
    >>> plt.show()  # doctest: +SKIP

    ... against a fitted model if it exists:
    >>> from sklearn.linear_model import LinearRegression
    >>> model = LinearRegression().fit(x, y)
    >>> s.plotter(model)
    >>> plt.show()  # doctest: +SKIP


    These can be used to run a full experimental cycle
    >>> from autora.experimentalist.pipeline import make_pipeline
    >>> from autora.experimentalist.pooler.grid import grid_pool
    >>> from autora.experimentalist.sampler.random_sampler import random_sampler
    >>> from functools import partial
    >>> import random
    >>> metadata = s.metadata
    >>> pool = partial(grid_pool, ivs=metadata.independent_variables)
    >>> random.seed(181) # set the seed for the random sampler
    >>> sampler = partial(random_sampler, n=20)
    >>> experimentalist_pipeline = make_pipeline([pool, sampler])

    >>> from autora.cycle import Cycle
    >>> theorist = LinearRegression()

    >>> cycle = Cycle(metadata=metadata, experimentalist=experimentalist_pipeline,
    ...               experiment_runner=s.experiment_runner, theorist=theorist)

    >>> c = cycle.run(10)
    >>> c.data.theories[-1].coef_   # doctest: +ELLIPSIS
    array([-0.53610647,  0.58457307])
"""

from autora.synthetic import data
from autora.synthetic.inventory import (
    Inventory,
    SyntheticExperimentCollection,
    describe,
    register,
    retrieve,
)