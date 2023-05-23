from typing import Any, TypedDict

class FoilXItem(TypedDict, total=False):
    """
    Data type for each item in X. May contain more properties.
    """
    imageId: int
    object_detect: dict
    panoptic_segmentation: dict[Any, Any]

FoilX = list[FoilXItem]
Foily = list[str]
FoilRules = dict[str, list[Any]]