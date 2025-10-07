from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class MaskedItem:
    c_mask: Any = field(default=None)
    c_group: Any = field(default=None)

    def set_c_mask(self, masks: List[Any]):
        self.c_mask = masks
        return self

    def get_c_mask(self):
        return self.c_mask

    def set_c_group(self, masks: List[Any]):
        self.c_group = masks
        return self

    def get_c_group(self):
        return self.c_group
