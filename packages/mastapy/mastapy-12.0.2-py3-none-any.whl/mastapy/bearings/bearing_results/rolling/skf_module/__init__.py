"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2038 import AdjustedSpeed
    from ._2039 import AdjustmentFactors
    from ._2040 import BearingLoads
    from ._2041 import BearingRatingLife
    from ._2042 import DynamicAxialLoadCarryingCapacity
    from ._2043 import Frequencies
    from ._2044 import FrequencyOfOverRolling
    from ._2045 import Friction
    from ._2046 import FrictionalMoment
    from ._2047 import FrictionSources
    from ._2048 import Grease
    from ._2049 import GreaseLifeAndRelubricationInterval
    from ._2050 import GreaseQuantity
    from ._2051 import InitialFill
    from ._2052 import LifeModel
    from ._2053 import MinimumLoad
    from ._2054 import OperatingViscosity
    from ._2055 import PermissibleAxialLoad
    from ._2056 import RotationalFrequency
    from ._2057 import SKFAuthentication
    from ._2058 import SKFCalculationResult
    from ._2059 import SKFCredentials
    from ._2060 import SKFModuleResults
    from ._2061 import StaticSafetyFactors
    from ._2062 import Viscosities
