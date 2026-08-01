import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("SimplePipeline")


class ValidationError(Exception):
    """Raised when the incoming data is missing required fields."""
    pass


@dataclass(frozen=True)
class CleanData:
    id: str
    price: float
    status: str

class DataTransformer(ABC):
    @abstractmethod
    def transform(self, raw_data: Dict[str, Any]) -> CleanData:
        pass                              
                                             
class PriceTransformer(DataTransformer):
    def transform(self, raw_data: Dict[str, Any]) -> CleanData:
        if "id" not in raw_data or "price" not in raw_data:
            raise ValidationError("Missing 'id' or 'price' fields.")
        
        try:
            clean_price = float(raw_data["price"]) * 1.15  
            
            return CleanData(
                id=str(raw_data["id"]),
                price=round(clean_price, 2),
                status="PROCESSED"
            )
        except (ValueError, TypeError) as error:
            raise ValidationError("Price must be a valid number.") from error

class Pipeline:
    def __init__(self, transformer:DataTransformer):
        self.transformer = transformer

    def process_all(self, data_list: List[Dict[str, Any]]) -> List[CleanData]:
        good_results = []
        
        for item in data_list:
            try:
                result = self.transformer.transform(item)
                good_results.append(result)
                logger.info(f"Successfully processed item {result.id}")
            except ValidationError as error:
                logger.warning(f"Skipping bad data: {error}")
                
        return good_results

if __name__ == "__main__":
    incoming_data = [
        {"id": "A101", "price": "100.00"},
        {"id": "B202", "price": "50.50"},
        {"broken_data": "no_fields_here"},
        {"id": "C303", "price": "not_a_number"}
    ]
   
    processor = PriceTransformer()
    app = Pipeline(transformer=processor)
    
    final_output = app.process_all(incoming_data)
    
    print("\n--- FINAL CLEAN DATA ---")
    for data in final_output:
        print(data)