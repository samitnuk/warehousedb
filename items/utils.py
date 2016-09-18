from .models import Item, Component, Product

CORE_X = {
    3: [],
    4: [],
    6: [124, 174, 224, 274, 324],
    8: []}

CONDUIT_X = {

    3: {"22": [],
        "23": [],
        "33": []},

    4: {"22": [],
        "23": [],
        "33": []},

    6: {"22": [272, 348, 424, 500, 578],
        "23": [254, 330, 406, 482, 560],
        "33": [236, 312, 388, 464, 542]},

    8: {"22": [],
        "23": [],
        "33": []}}

ROD_X = {
    3: "     -{}",
    4: "40303-{}",
    6: "70591-{}",
    8: "     -{}"}

SLEEVE_X = {
    3: "     -{}",
    4: "40004-{}",
    6: "60004-{}",
    8: "     -{}"}

HUB_X = {

    3: {"22": [],
        "23": [],
        "33": []},

    4: {"22": ["40024-20"],
        "23": ["40024-20", "40023-20"],
        "33": ["40023-20"]},

    6: {"22": ["60024-20"],
        "23": ["60024-20", "60023-20"],
        "33": ["60023-20"]},

    8: {"22": [],
        "23": [],
        "33": []}}

NUT_X_s = {             # nut on rods (s - small)
    3: "Гайка М5",
    4: "Гайка М6",
    6: "Гайка М8",
    8: "Гайка М10"}

NUT_X_b = {             # nut on hubs (b - big)
    3: "Гайка М12",
    4: "Гайка М16х1,5",
    6: "Гайка М18х1,5",
    8: "Гайка М22"}

WASHER_X = {
    3: "Шайба М12",
    4: "Шайба М16",
    6: "Шайба М18",
    8: "Шайба М22"}


def create_std_cable(core_id, conduit_id, serie, travel, mounting, length):

    items = Item.objects.all()

    cable = Product.objects.create(
        title="Трос дистанційного управління",
        part_number="100.M{0}{1}{2}.{3:0>5}".format(travel, mounting, length),
        notes="#{} Стандартний трос 'тягни-штовхай'".format(serie))

    # core
    core = items.filter(pk=core_id).first()
    Component.objects.create(
        product=cable,
        item=core,
        quantity=(length - CORE_X[6][travel]))

    # conduit
    conduit = items.filter(pk=int(conduit_id)).first()
    Component.objects.create(
        product=cable,
        item=conduit,
        quantity=(length - CONDUIT_X[6][mounting][travel]))

    # rod
    rod = items.filter(part_number=ROD_X[serie].format(travel)).first()
    Component.objects.create(
        product=cable,
        item=rod,
        quantity=2)

    # sleeve
    sleeve = items.filter(part_number=SLEEVE_X[serie].format(travel)).first()
    Component.objects.create(
        product=cable,
        item=sleeve,
        quantity=2)

    # hub
    for part_number in HUB_X[serie][mounting]:
        hub = items.filter(part_number=part_number).first()
        Component.objects.create(
            product=cable,
            item=hub,
            quantity=2 if mounting in ["22", "33"] else 1)

    # nut (small)
    nut = items.filter(title=NUT_X_s[serie]).first()
    Component.objects.create(
        product=cable,
        item=nut,
        quantity=2)

    # nut (big)
    if mounting in ["22", "23"]:
        nut = items.filter(title=NUT_X_b[serie]).first()
        Component.objects.create(
            product=cable,
            item=nut,
            quantity=2 if mounting == "22" else 1)

    # washer
    if mounting in ["22", "23"]:
        washer = items.filter(title=WASHER_X[serie]).first()
        Component.objects.create(
            product=cable,
            item=washer,
            quantity=2 if mounting == "22" else 1)

    return cable
