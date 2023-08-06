from mines_data_engineering.relalg import *

SmallZips = Relation("Zips",
          [Attribute("loc", str), Attribute("zip", int)],
          [("Denver", 80114), ("Denver", 80115), ("Lakewood", 80228), ("Golden", 80401)]
         )

SmallStops = Relation("Stops",
    [Attribute("loc", str), Attribute("cit", bool)],
    [("Golden", False), ("Denver", True),("Denver", False), ("Lakewood", True)]
)

BigZips = Relation("BigZips",
[Attribute("loc", str), Attribute("zip", int)], [])
BigZips.generate_records(10_000, [city_generator, None])

BigStops = Relation("BigStops",
    [Attribute("loc", str), Attribute("cit", bool)], [])
BigStops.generate_records(10_000, [city_generator, None])

BigZips2 = sort(BigZips, [0]).materialize()
BigStops2 = sort(BigStops, [0]).materialize()
