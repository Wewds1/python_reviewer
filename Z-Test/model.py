from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, Set


@dataclass(frozen=True)
class Orderline:
    orderid: str
    sku: str
    qty: int
    
    
class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.ref = ref
        self.sku = sku
        self._purchased_quantity = qty
        self.eta = eta
        self._allocations: Set[Orderline] = set()


    def allocate(self, line: Orderline):
        self.available_quantity -= line.qty
        
        
    def can_allocate(self, line: Orderline) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    
    def deallocate(self, line: Orderline):
        if line in self._allocations:
            self._allocations.remove(line)
            
        
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity
