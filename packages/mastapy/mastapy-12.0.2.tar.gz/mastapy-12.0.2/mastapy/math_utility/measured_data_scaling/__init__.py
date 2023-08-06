"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1536 import DataScalingOptions
    from ._1537 import DataScalingReferenceValues
    from ._1538 import DataScalingReferenceValuesBase
