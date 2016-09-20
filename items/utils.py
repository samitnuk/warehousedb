from .models import Item, Component, Product

# reserve for cutting
cutting = 15

CORE_X = {
    3: [],
    4: [124, 174, 224, 274, 324],
    6: [130, 180, 230, 280, 330],
    8: []}

CONDUIT_X = {

    3: {"22": [],
        "23": [],
        "33": []},

    4: {"22": [272, 348, 424, 500, 578],
        "23": [254, 330, 406, 482, 560],
        "33": [236, 312, 388, 464, 542]},

    6: {"22": [278, 354, 430, 506, 582],
        "23": [256, 332, 408, 484, 560],
        "33": [234, 310, 386, 462, 538]},

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

NUT_X_s = {  # nut on rods (s - small)
    3: "Гайка М5",
    4: "Гайка М6",
    6: "Гайка М8",
    8: "Гайка М10"}

NUT_X_b = {  # nut on hubs (b - big)
    3: "Гайка низька М12",
    4: "Гайка низька М16х1.5",
    6: "Гайка низька М18х1.5",
    8: "Гайка низька М22"}

WASHER_X = {
    3: "Шайба М12",
    4: "Шайба М16",
    6: "Шайба М18",
    8: "Шайба М22"}


def create_std_cable(core_id, conduit_id, serie, travel, mounting, length):
    serie = int(serie)
    travel = int(travel)

    items = Item.objects.all()

    cable = Product.objects.create(
        title="Трос дистанційного управління",
        part_number="100.M{0}{1}{2}.{3:0>5}".format(
            serie, travel, mounting, length),
        notes="#{} Стандартний трос 'тягни-штовхай'".format(serie))

    # core
    core = items.filter(pk=core_id).first()
    print(core)
    Component.objects.create(
        product=cable,
        item=core,
        quantity=(length - CORE_X[serie][travel - 1] + cutting))

    # conduit
    conduit = items.filter(pk=int(conduit_id)).first()
    Component.objects.create(
        product=cable,
        item=conduit,
        quantity=(length - CONDUIT_X[serie][mounting][travel - 1] + cutting))

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
    print(nut)
    Component.objects.create(
        product=cable,
        item=nut,
        quantity=2)

    # nut (big)
    if mounting in ["22", "23"]:
        nut = items.filter(title=NUT_X_b[serie]).first()
        print(nut)
        Component.objects.create(
            product=cable,
            item=nut,
            quantity=4 if mounting == "22" else 2)

    # washer
    if mounting in ["22", "23"]:
        washer = items.filter(title=WASHER_X[serie]).first()
        Component.objects.create(
            product=cable,
            item=washer,
            quantity=4 if mounting == "22" else 2)

    return cable
