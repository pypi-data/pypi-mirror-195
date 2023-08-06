from dataclasses import dataclass, field
from typing import Any, List, Optional
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(frozen=True)
class BinType:
    """BinType data class"""
    code: str = field(metadata=config(field_name="Code"))
    size: float = field(metadata=config(field_name="Size"))
    unit: str = field(metadata=config(field_name="Unit"))
    containerType: str = field(metadata=config(field_name="ContainerType"))


@dataclass_json
@dataclass(frozen=True)
class Fee:
    """Fee data class"""
    description: str = field(metadata=config(field_name="Description"))
    binType: Optional[BinType] = field(metadata=config(field_name="BinType"))
    wastePickupsPerYear: int = field(metadata=config(field_name="WastePickupsPerYear"))
    wastePickupFrequency: Optional[str] = field(metadata=config(field_name="WastePickupFrequency"))
    wastePickupFrequency_code: Optional[str] = field(metadata=config(field_name="WastePickupFrequencyCode"))
    changeSizeOfBinText: Optional[str] = field(metadata=config(field_name="ChangeSizeOfBinText"))
    changeFrequencyText: Optional[str] = field(metadata=config(field_name="ChangeFrequencyText"))
    wasteType: str = field(metadata=config(field_name="WasteType"))
    code: str = field(metadata=config(field_name="Code"))
    product: str = field(metadata=config(field_name="Product"))
    partProduct: str = field(metadata=config(field_name="PartProduct"))
    designation: str = field(metadata=config(field_name="Designation"))
    calculatedCost: int = field(metadata=config(field_name="CalculatedCost"))
    isCostCalculated: bool = field(metadata=config(field_name="IsCostCalculated"))
    partYearStarts: str = field(metadata=config(field_name="PartYearStarts"))
    partYearEnds: str = field(metadata=config(field_name="PartYearEnds"))
    partYearDescription: str = field(metadata=config(field_name="PartYearDescription"))
    id: int = field(metadata=config(field_name="ID"))


@dataclass_json
@dataclass(frozen=True)
class RhService:
    """RhService data class, base object"""
    nextWastePickup: str = field(metadata=config(field_name="NextWastePickup"))
    wastePickupsPerYear: int = field(metadata=config(field_name="WastePickupsPerYear"))
    wasteType: str = field(metadata=config(field_name="WasteType"))
    wastePickupFrequency: str = field(metadata=config(field_name="WastePickupFrequency"))
    wastePickupFrequencyCode: str = field(metadata=config(field_name="WastePickupFrequencyCode"))
    binType: BinType = field(metadata=config(field_name="BinType"))
    numberOfBins: float = field(metadata=config(field_name="NumberOfBins"))
    fee: Fee = field(metadata=config(field_name="Fee"))
    numberOfBinsAntl: int = field(metadata=config(field_name="NumberOfBinsAntl"))
    isActive: bool = field(metadata=config(field_name="IsActive"))
    id: int = field(metadata=config(field_name="ID"))
    description: str = field(metadata=config(field_name="Description"))
    startDate: str = field(metadata=config(field_name="StartDate"))
    stopDate: str = field(metadata=config(field_name="StopDate"))
    buildingId: str = field(metadata=config(field_name="BuildingID"))


@dataclass_json
@dataclass(frozen=True)
class RhServices:
    services: List[RhService] = field(metadata=config(field_name="RhServices"))


@dataclass_json
@dataclass(frozen=True)
class SearchAddressResult:
    """TypeDef for SearchAddressResult query"""
    succeeded: bool = field(metadata=config(field_name="Succeeded"))
    buildings: List[str] = field(metadata=config(field_name="Buildings"))
