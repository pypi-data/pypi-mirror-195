import numpy as np

from abc import abstractmethod
from typing import Union


class GLIDEError(Exception):
    """Raised when an error related to the ASF classes is encountered.
    """


class GLIDEBase:
    """
    Implements the non-differentiable variant of GLIDE-II as proposed in
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Note:
        Additional contraints produced by the GLIDE-II formulation are implemented
        such that if the returned values are negative, the corresponding constraint is
        violated. The returned value may be positive. In such cases, the returned value
        is a measure of how close or far the corresponding feasible solution is from
        violating the constraint.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):

        self.has_additional_constraints = False
        self.utopian = utopian
        self.nadir = nadir
        self.rho = rho
        self.required_keys: dict = {}
        self.extras = kwargs

    def __call__(self, objective_vector: np.ndarray, preference: dict) -> np.ndarray:
        """Evaluate the scalarization function value based on objective vectors and
        DM preference.

        Args:
            objective_vector (np.ndarray): 2-dimensional array of objective values of solutions.
            preference (dict): The preference given by the decision maker. The required
                dictionary keys and their meanings can be found in self.required_keys variable.

        Returns:
            np.ndarray: The scalarized value obtained by using GLIDE-II over
                objective_vector.
        """
        self.preference = preference
        self.objective_vector = np.atleast_2d(objective_vector)

        f_minus_q = self.objective_vector - self.q
        mu = np.atleast_2d(self.mu)
        I_alpha = self.I_alpha

        max_term = np.max(mu[:, I_alpha] * f_minus_q[:, I_alpha], axis=1)
        sum_term = self.rho * np.sum(self.w * f_minus_q, axis=1)
        return max_term + sum_term

    def evaluate_constraints(
        self, objective_vector: np.ndarray, preference: dict
    ) -> Union[None, np.ndarray]:
        # TODO: Description for Args & Returns are yet to be filled.
        """Evaluate the additional contraints generated by the GLIDE-II formulation.

        Note:
            Additional contraints produced by the GLIDE-II formulation are implemented
            such that if the returned values are negative, the corresponding constraint is
            violated. The returned value may be positive. In such cases, the returned value
            is a measure of how close or far the corresponding feasible solution is from
            violating the constraint.

        Args:
            objective_vector (np.ndarray): [description]
            preference (dict): [description]

        Returns:
            Union[None, np.ndarray]: [description]
        """
        if not self.has_additional_constraints:
            return None

        self.preference = preference
        self.objective_vector = np.atleast_2d(objective_vector)

        constraints = (
            self.epsilon[self.I_epsilon]
            + self.s_epsilon * self.delta_epsilon[self.I_epsilon]
            - self.objective_vector[:, self.I_epsilon]
        )

        return constraints

    @property
    @abstractmethod
    def I_alpha(self):
        pass

    @property
    @abstractmethod
    def I_epsilon(self):
        pass

    @property
    @abstractmethod
    def mu(self):
        pass

    @property
    @abstractmethod
    def q(self):
        pass

    @property
    @abstractmethod
    def w(self):
        pass

    @property
    @abstractmethod
    def epsilon(self):
        pass

    @property
    @abstractmethod
    def s_epsilon(self):
        pass

    @property
    @abstractmethod
    def delta_epsilon(self):
        pass


class reference_point_method_GLIDE(GLIDEBase):
    """
    Implements the reference point method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=nadir, rho=rho, **kwargs)
        self.has_additional_constraints = False
        self.__I_alpha = np.full_like(
            utopian, dtype=np.bool_, fill_value=True
        ).flatten()
        self.__I_epsilon = np.full_like(
            utopian, dtype=np.bool_, fill_value=False
        ).flatten()
        self.__w = 1
        self.__mu = 1 / (nadir - utopian)
        self.required_keys = {
            "reference point": (
                "Used to calculate the direction of improvement: "
                "a line parallel to the nadir-utopian vector "
                "and passing through the reference point. "
                "(type: numpy.ndarray)"
            )
        }

    @property
    def I_epsilon(self):
        return self.__I_epsilon

    @property
    def I_alpha(self):
        return self.__I_alpha

    @property
    def mu(self):
        return self.__mu

    @property
    def w(self):
        return self.__w

    @property
    def q(self):
        return self.preference["reference point"]

    @property
    def epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def s_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def delta_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)


class GUESS_GLIDE(GLIDEBase):
    """
    Implements the GUESS method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=nadir, rho=rho, **kwargs)
        self.has_additional_constraints = False
        self.__I_alpha = np.full_like(
            utopian, dtype=np.bool_, fill_value=True
        ).flatten()
        self.__I_epsilon = np.full_like(
            utopian, dtype=np.bool_, fill_value=False
        ).flatten()
        self.__w = 0
        self.required_keys = {
            "reference point": (
                "Used to calculate the direction of improvement: "
                "a line going from the nadir point to the reference point. "
                "(type: numpy.ndarray)"
            )
        }

    @property
    def I_epsilon(self):
        return self.__I_epsilon

    @property
    def I_alpha(self):
        return self.__I_alpha

    @property
    def mu(self):
        return 1 / (self.nadir - self.preference["reference point"])

    @property
    def w(self):
        return self.__w

    @property
    def q(self):
        return self.preference["reference point"]

    @property
    def epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def s_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def delta_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)


class AUG_GUESS_GLIDE(GUESS_GLIDE):
    """
    Implements the Augmented GUESS method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=nadir, rho=rho, **kwargs)
        self.__w = 1


class NIMBUS_GLIDE(GLIDEBase):
    """
    Implements the NIMBUS method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=nadir, rho=rho, **kwargs)

        self.__mu = self.__w = 1 / (self.nadir - self.utopian)

        self.has_additional_constraints = True
        self.required_keys = {
            "current solution": (
                "A solution preferred by the DM currently. " "(type: numpy.ndarray)"
            ),
            "classifications": (
                "A list of same length as the number of objectives. Elements can only "
                "include some or all of ['<', '<=', '=', '>=', '0']. These classify "
                "the different objectives as defined in the NIMBUS or GLIDE-II paper. "
                "(type: list)"
            ),
            "levels": (
                "A vector containing desirable levels of objectives or constraining bounds "
                "depending on the classification. Same length as the number of objectives. "
                "(type: numpy.ndarray)"
            ),
        }

    @property
    def improve_unconstrained(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == "<")[0]
        indices[relevant] = True
        return indices

    @property
    def improve_constrained(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == "<=")[0]
        indices[relevant] = True
        return indices

    @property
    def satisfactory(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == "=")[0]
        indices[relevant] = True
        return indices

    @property
    def relax_constrained(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == ">=")[0]
        indices[relevant] = True
        return indices

    @property
    def relax_unconstrained(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == "0")[0]
        indices[relevant] = True
        return indices

    @property
    def I_alpha(self):
        return self.improve_unconstrained + self.improve_constrained

    @property
    def I_epsilon(self):
        return (
            self.improve_unconstrained
            + self.improve_constrained
            + self.satisfactory
            + self.relax_constrained
        )

    @property
    def w(self):
        # This was in the paper
        return self.__w
        # This is what I think it should be. There may be division by zero errors here.
        """return (self.objective_vector / (self.objective_vector - self.q)) / (
            self.nadir - self.utopian
        )"""

    @property
    def mu(self):
        return self.__mu

    @property
    def q(self):
        q = np.full_like(self.utopian, fill_value=0, dtype=float)
        q[self.improve_unconstrained] = self.utopian[self.improve_unconstrained]
        q[self.improve_constrained] = self.preference["levels"][
            self.improve_constrained
        ]
        return q

    @property
    def epsilon(self):
        e = np.full_like(self.utopian, fill_value=np.nan, dtype=float)

        case1 = (
            self.improve_constrained + self.improve_unconstrained + self.satisfactory
        )
        case2 = self.relax_constrained

        e[case1] = self.preference["current solution"][case1]
        e[case2] = self.preference["levels"][case2]
        return e

    @property
    def s_epsilon(self):
        return 0

    @property
    def delta_epsilon(self):
        return np.zeros_like(self.utopian)


class STEP_GLIDE(GLIDEBase):
    """
    Implements the STEP method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=nadir, rho=rho, **kwargs)
        self.__mu = (self.nadir - self.utopian) / np.max(
            np.abs(np.vstack((utopian, nadir))), axis=0
        )
        self.__w = 0

        self.I_epsilon = np.full_like(self.utopian, dtype=np.bool_, fill_value=True)

        self.has_additional_constraints = True
        self.required_keys = {
            "current solution": (
                "A solution preferred by the DM currently. " "(type: numpy.ndarray)"
            ),
            "classifications": (
                "A list of same length as the number of objectives. Elements can only "
                "include some or all of [<=', '=', '>=']. These classify "
                "the different objectives as defined in the GLIDE-II paper. "
                "(type: list)"
            ),
            "levels": (
                "A vector containing desirable levels of objectives or constraining bounds "
                "depending on the classification. Same length as the number of objectives. "
                "(type: numpy.ndarray)"
            ),
        }

    @property
    def improve_constrained(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == "<=")[0]
        indices[relevant] = True
        return indices

    @property
    def satisfactory(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == "=")[0]
        indices[relevant] = True
        return indices

    @property
    def relax_constrained(self):
        indices = np.full_like(self.utopian, dtype=np.bool_, fill_value=False)
        relevant = np.where(np.array(self.preference["classifications"]) == ">=")[0]
        indices[relevant] = True
        return indices

    @property
    def I_alpha(self):
        return self.improve_constrained

    @property
    def w(self):
        # This was in the paper
        return self.__w

    @property
    def mu(self):
        return self.__mu

    @property
    def q(self):
        q = np.full_like(self.utopian, fill_value=0, dtype=float)
        q[self.improve_constrained] = self.utopian[self.improve_constrained]
        return q

    @property
    def epsilon(self):
        e = np.full_like(self.utopian, fill_value=np.nan, dtype=float)

        case1 = self.improve_constrained + self.satisfactory
        case2 = self.relax_constrained

        e[case1] = self.preference["current solution"][case1]
        e[case2] = self.preference["levels"][case2]
        return e

    @property
    def s_epsilon(self):
        return 0

    @property
    def delta_epsilon(self):
        return np.zeros_like(self.utopian)


class STOM_GLIDE(GLIDEBase):
    """
    Implements the STOM method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Has no effect on STOM calculation. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=None, rho=rho, **kwargs)
        self.has_additional_constraints = False
        self.__I_alpha = np.full_like(
            utopian, dtype=np.bool_, fill_value=True
        ).flatten()
        self.__I_epsilon = np.full_like(
            utopian, dtype=np.bool_, fill_value=False
        ).flatten()
        self.__w = 0
        self.required_keys = {
            "reference point": (
                "Used to calculate the direction of improvement: "
                "a line going from the reference point to the utopian point. "
                "(type: numpy.ndarray)"
            )
        }

    @property
    def I_epsilon(self):
        return self.__I_epsilon

    @property
    def I_alpha(self):
        return self.__I_alpha

    @property
    def mu(self):
        return 1 / (self.preference["reference point"] - self.utopian)

    @property
    def w(self):
        return self.__w

    @property
    def q(self):
        return self.utopian

    @property
    def epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def s_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def delta_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)


class AUG_STOM_GLIDE(STOM_GLIDE):
    """
    Implements the Augmented STOM method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Has no effect on STOM calculation. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=None, rho=rho, **kwargs)
        self.has_additional_constraints = False
        self.__w = 1


class Tchebycheff_GLIDE(GLIDEBase):
    """
    Implements the Tchebycheff method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self,
        utopian: np.ndarray = None,
        nadir: np.ndarray = None,
        rho: float = 1e-6,
        **kwargs
    ):
        super().__init__(utopian=utopian, nadir=None, rho=rho, **kwargs)
        self.has_additional_constraints = False
        self.__I_alpha = np.full_like(
            utopian, dtype=np.bool_, fill_value=True
        ).flatten()
        self.__I_epsilon = np.full_like(
            utopian, dtype=np.bool_, fill_value=False
        ).flatten()
        self.__w = 1
        self.required_keys = {
            "mu": (
                "Vector defining the direction of improvement of the scalarizer. "
                "(type: numpy.ndarray)"
            )
        }

    @property
    def I_epsilon(self):
        return self.__I_epsilon

    @property
    def I_alpha(self):
        return self.__I_alpha

    @property
    def mu(self):
        return self.preference["mu"]

    @property
    def w(self):
        return self.__w

    @property
    def q(self):
        return self.utopian

    @property
    def epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def s_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def delta_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)


class PROJECT_GLIDE(GLIDEBase):
    """
    Implements the PROJECT method of preference elicitation and scalarization
    using the non-differentiable variant of GLIDE-II as proposed in:
    Ruiz, Francisco, Mariano Luque, and Kaisa Miettinen.
    "Improving the computational efficiency in a global formulation (GLIDE)
    for interactive multiobjective optimization."
    Annals of Operations Research 197.1 (2012): 47-70.

    Args:
        utopian (np.ndarray, optional): The utopian point. Defaults to None.
        nadir (np.ndarray, optional): The nadir point. Defaults to None.
        rho (float, optional): The augmentation term for the scalarization function.
            Defaults to 1e-6.
    """

    def __init__(
        self, current_objective_vector: np.ndarray, rho: float = 1e-6, **kwargs
    ):
        super().__init__(utopian=None, nadir=None, rho=rho, **kwargs)
        self.current_objective_vector = current_objective_vector
        self.has_additional_constraints = False
        self.__I_alpha = np.full_like(
            current_objective_vector, dtype=np.bool_, fill_value=True
        ).flatten()
        self.__I_epsilon = np.full_like(
            current_objective_vector, dtype=np.bool_, fill_value=False
        ).flatten()
        self.__w = 0

    @property
    def I_epsilon(self):
        return self.__I_epsilon

    @property
    def I_alpha(self):
        return self.__I_alpha

    @property
    def mu(self):
        return 1 / np.abs(
            self.preference["reference point"] - self.current_objective_vector
        )

    @property
    def w(self):
        return self.__w

    @property
    def q(self):
        return self.utopian

    @property
    def epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def s_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)

    @property
    def delta_epsilon(self):
        msg = "This part of the code should not be reached. Contact maintaner."
        raise GLIDEError(msg)
