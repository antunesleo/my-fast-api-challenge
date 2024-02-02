import factory


class LocationDBFactory(factory.DictFactory):
    latitude = 45.45
    longitude = 46.46


class PlaceDBFactory(factory.DictFactory):
    name = "name"
    description = "description"
    location = factory.SubFactory(LocationDBFactory)
