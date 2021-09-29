from dataclasses import dataclass, field
import random
import pydantic


class City:
    name: str
    population: int
    growth: int
    wealth: float
    income: float
    # thing: Optional[str]


city_list = []
city_names = [f"Abergavenny", f"Tewkesbury", f"Oxted", f"Burton", f"Wellis", f"Hawarden", f"Chirbury", f"Neath", f"Caerwent", f"Margam", f"Caerleon", f"Harlech", f"Axbridge"]

def random_city():
    r = random.choice(city_names)
    city_names.remove(r)
    city_list.append(r)
    return r





