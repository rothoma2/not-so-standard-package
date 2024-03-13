from typing import List
from pydantic import BaseModel

class Features(BaseModel):   
    package_id: str
    package_name: str
    file_name: str
    # quantitative features
    shanon_entropy__file:float # entropy of the entire file
    # the quantities below are based on statistics of each line in the file
    shanon_entropy__number_outliers: int
    shanon_entropy__mean: float
    shanon_entropy__median: float
    shanon_entropy__variance: float
    shanon_entropy__max: float
    shanon_entropy__1Q: float
    shanon_entropy__3Q: float


    