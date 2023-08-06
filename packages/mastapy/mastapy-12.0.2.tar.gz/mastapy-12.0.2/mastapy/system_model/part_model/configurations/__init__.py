"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2566 import ActiveFESubstructureSelection
    from ._2567 import ActiveFESubstructureSelectionGroup
    from ._2568 import ActiveShaftDesignSelection
    from ._2569 import ActiveShaftDesignSelectionGroup
    from ._2570 import BearingDetailConfiguration
    from ._2571 import BearingDetailSelection
    from ._2572 import PartDetailConfiguration
    from ._2573 import PartDetailSelection
