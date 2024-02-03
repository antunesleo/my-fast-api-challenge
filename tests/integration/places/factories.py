import factory


class LocationDBFactory(factory.DictFactory):
    latitude = 45.45
    longitude = 46.46


class PlaceDBFactory(factory.DictFactory):
    name = factory.Sequence(lambda n: "Name {}".format(n))
    description = factory.Sequence(lambda n: "Description {}".format(n))
    location = factory.SubFactory(LocationDBFactory)
