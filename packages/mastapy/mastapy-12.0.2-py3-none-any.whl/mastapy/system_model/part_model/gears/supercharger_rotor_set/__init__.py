"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2510 import BoostPressureInputOptions
    from ._2511 import InputPowerInputOptions
    from ._2512 import PressureRatioInputOptions
    from ._2513 import RotorSetDataInputFileOptions
    from ._2514 import RotorSetMeasuredPoint
    from ._2515 import RotorSpeedInputOptions
    from ._2516 import SuperchargerMap
    from ._2517 import SuperchargerMaps
    from ._2518 import SuperchargerRotorSet
    from ._2519 import SuperchargerRotorSetDatabase
    from ._2520 import YVariableForImportedData
