from .models import ThirdAdministrativeLevel, FirstAdministrativeLevel

natural_keys = [
    ("ETH", 10, 66, 600),
    ("ETH", 3, 14,  123),
    ("ETH", 10, 67, 606),
    ("ETH", 3, 7, 46),
    ("ETH", 8, 41, 430),
    ("ETH", 10, 71, 628),
    ("ETH", 4, 21, 187),
    ("ETH", 4, 21, 187),
    ("ETH", 3, 11, 67),
    ("ETH", 3, 11, 67),
    ("ETH", 2, 4, 31),
    ("ETH", 2, 4, 31),
    ("LBY", 15),
]


for k in natural_keys:
    for i in ThirdAdministrativeLevel.objects.all():
        if i.natural_key() == k:
            print(i.id, i, i.fake_id, i.natural_key())

    for i in FirstAdministrativeLevel.objects.all():
        if i.natural_key() == k:
            print(i.id, i, i.fake_id, i.natural_key())
