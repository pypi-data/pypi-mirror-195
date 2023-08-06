"""__init__.py"""


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5612 import AbstractAssemblyStaticLoadCaseGroup
    from ._5613 import ComponentStaticLoadCaseGroup
    from ._5614 import ConnectionStaticLoadCaseGroup
    from ._5615 import DesignEntityStaticLoadCaseGroup
    from ._5616 import GearSetStaticLoadCaseGroup
    from ._5617 import PartStaticLoadCaseGroup
