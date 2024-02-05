import factory


class LocationDBFactory(factory.DictFactory):
    type = "Point"
    coordinates = [46.46, 45.45]


class PlaceDBFactory(factory.DictFactory):
    name = factory.Sequence(lambda n: "Name {}".format(n))
    description = factory.Sequence(lambda n: "Description {}".format(n))
    location = factory.SubFactory(LocationDBFactory)
