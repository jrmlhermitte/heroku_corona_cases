from dataclasses import dataclass
from typing import Optional


# Maybe overkill but still good separation of concerns
@dataclass
class NumericalRange:
    start: float
    end: float
    include_endpoint: bool = False

    def within_bounds(self, value: float):
        if value < self.start:
            return False
        if value > self.end:
            return False
        if value != self.end:
            return True
        if self.include_endpoint and value == self.end:
            return True
        return False

    def to_text(self, round_to_decimal: Optional[int] = None) -> str:
        start = self.start
        end = self.end
        if round_to_decimal is not None:
            start = round(start, round_to_decimal)
            end = round(end, round_to_decimal)
            if round_to_decimal <= 0:
                start = int(start)
                end = int(end)
        message = f"{start} <= X "
        if self.include_endpoint:
            message += "="
        message += f"< {end}"
        return message
