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
    3: "Гайка М12 низька",
    4: "Гайка М16х1,5 низька",
    6: "Гайка М18х1,5 низька",
    8: "Гайка М22 низька"}

WASHER_X = {
    3: "Шайба 12",
    4: "Шайба 16",
    6: "Шайба 18",
    8: "Шайба 22"}

ROD_SEAL = {
    3: "",
    4: "40008-С",
    6: "60008-С",
    8: ""}

SLEEVE_SEAL = {
    3: "",
    4: "40324-1",
    6: "60009-1-С",
    8: ""}

BEARING = {
    3: "",
    4: "40009-1-С",
    6: "60317-1",
    8: ""}


def create_std_cable(
    conduit_id, core_id, serie, travel, mounting,
    is_steel_rods, is_steel_sleeves, length
):

    items = Item.objects.all()
    serie = int(serie)
    travel = int(travel)
    notes = "#{} Стандартний трос 'тягни-штовхай'".format(serie)

    if is_steel_rods:
        notes = ", ".join([notes, "прутки з чорної сталі"])
        rod_part_number = "".join([ROD_X[serie].format(travel), "ст"])
    else:
        rod_part_number = ROD_X[serie].format(travel)

    if is_steel_sleeves:
        notes = ", ".join([notes, "трубки з чорної сталі"])
        sleeve_part_number = "".join([SLEEVE_X[serie].format(travel), "ст"])
    else:
        sleeve_part_number = SLEEVE_X[serie].format(travel)

    cable = Product.objects.create(
        title="ТДУ",
        part_number="100.M{0}{1}{2}.{3:0>5}".format(
            serie, travel, mounting, length),
        notes=notes)

    # core
    Component.objects.create(
        product=cable,
        item=items.filter(pk=core_id).first(),
        quantity=(length - CORE_X[serie][travel - 1] + cutting))

    # conduit
    Component.objects.create(
        product=cable,
        item=items.filter(pk=int(conduit_id)).first(),
        quantity=(length - CONDUIT_X[serie][mounting][travel - 1] + cutting))

    # rod
    Component.objects.create(
        product=cable,
        item=items.filter(part_number=rod_part_number).first(),
        quantity=2)

    # sleeve
    Component.objects.create(
        product=cable,
        item=items.filter(part_number=sleeve_part_number).first(),
        quantity=2)

    # hub
    for part_number in HUB_X[serie][mounting]:
        Component.objects.create(
            product=cable,
            item=items.filter(part_number=part_number).first(),
            quantity=2 if mounting in ["22", "33"] else 1)

    # nut (small)
    Component.objects.create(
        product=cable,
        item=items.filter(title=NUT_X_s[serie]).first(),
        quantity=2)

    # nut (big)
    if mounting in ["22", "23"]:
        Component.objects.create(
            product=cable,
            item=items.filter(title=NUT_X_b[serie]).first(),
            quantity=4 if mounting == "22" else 2)

    # washer
    if mounting in ["22", "23"]:
        Component.objects.create(
            product=cable,
            item=items.filter(title=WASHER_X[serie]).first(),
            quantity=4 if mounting == "22" else 2)

    # rod seal
    Component.objects.create(
        product=cable,
        item=items.filter(part_number=ROD_SEAL[serie]).first(),
        quantity=2)

    # sleeve seal
    Component.objects.create(
        product=cable,
        item=items.filter(part_number=ROD_SEAL[serie]).first(),
        quantity=2)

    # bearing
    if serie in [3, 4, 6]:
        Component.objects.create(
            product=cable,
            item=items.filter(part_number=BEARING[serie]).first(),
            quantity=2)


def create_tza_cable(core_id, conduit_id, is_steel_rods, length):

    items = Item.objects.all()
    notes = ""

    if is_steel_rods:
        notes = "прутки з чорної сталі"
        rod1_part_number = "40303-ТЗАст"
        rod2_part_number = "40303-5ст"
    else:
        rod1_part_number = "40303-ТЗА"
        rod2_part_number = "40303-5"

    cable = Product.objects.create(
        title="Трос ТЗА",
        part_number="ТЗА-100.М4(110)20.{:0>5}-01".format(length),
        notes=notes)

    # core
    core = Item.objects.filter(pk=core_id).first()
    Component.objects.create(
        product=cable,
        item=core,
        quantity=(length - 282 + cutting))

    # conduit
    conduit = Item.objects.filter(pk=int(conduit_id)).first()
    Component.objects.create(
        product=cable,
        item=conduit,
        quantity=(length - 443 + cutting))

    # nut (small)
    Component.objects.create(
        product=cable,
        item=items.filter(title="Гайка М6").first(),
        quantity=2)

    # nut (big)
    Component.objects.create(
        product=cable,
        item=items.filter(title="Гайка М12х1,25 низька").first(),
        quantity=2)

    # union nut
    Component.objects.create(
        product=cable,
        item=items.filter(part_number="40013-ТЗА").first(),
        quantity=1)

    # hub
    Component.objects.create(
        product=cable,
        item=items.filter(part_number="40020-ТЗА").first(),
        quantity=2)

    # tube 01
    Component.objects.create(
        product=cable,
        item=items.filter(part_number="40004-ТЗА-01").first(),
        quantity=1)

    # tube 02
    Component.objects.create(
        product=cable,
        item=items.filter(part_number="40004-ТЗА-02").first(),
        quantity=1)

    # rod 01
    Component.objects.create(
        product=cable,
        item=items.filter(part_number=rod1_part_number).first(),
        quantity=1)

    # rod 02
    Component.objects.create(
        product=cable,
        item=items.filter(part_number=rod2_part_number).first(),
        quantity=1)

    # seal
    Component.objects.create(
        product=cable,
        item=items.filter(part_number="425138СР-03").first(),
        quantity=1)

    # # flange bearing
    # Component.objects.create(
    #     product=cable,
    #     item=items.filter(part_number="FB01-12").first(),
    #     quantity=1)


def base_for_H_cables(cable, is_steel_rod_E):

    # hub
    Component.objects.create(
        product=cable,
        item=Item.objects.filter(part_number="40025-20").first(),
        quantity=1)

    # flange
    Component.objects.create(
        product=cable,
        item=Item.objects.filter(part_number="Г002", title="Фланець").first(),
        quantity=1)

    # body
    Component.objects.create(
        product=cable,
        item=Item.objects.filter(part_number="Г-001", title="Стакан").first(),
        quantity=1)

    if is_steel_rod_E:
        rod_part_number = "40303-Ест"
    else:
        rod_part_number = "40303-Е"

    # body
    Component.objects.create(
        product=cable,
        item=Item.objects.filter(part_number=rod_part_number).first(),
        quantity=1)


def create_H4_cable(
    core_id,
    conduit_id,
    is_steel_rod_E,
    length
):

    items = Item.objects.all()
    notes = ""

    if is_steel_rod_E:
        notes = "Пруток 40303-Ест (чорна сталь)"

    cable = Product.objects.create(
        title="Трос Г4 (МТЗ)",
        part_number="100.М4(40)Г4.{:0>5}".format(length),
        notes=notes)

    base_for_H_cables(cable, is_steel_rod_E)

    # # core
    # Component.objects.create(
    #     product=cable,
    #     item=items.filter(pk=core_id).first(),
    #     quantity=(length - ___ + cutting))

    # # conduit
    # Component.objects.create(
    #     product=cable,
    #     item=items.filter(pk=int(conduit_id)).first(),
    #     quantity=(length - ___ + cutting))

    # nut (small)
    Component.objects.create(
        product=cable,
        item=items.filter(title="Гайка М6").first(),
        quantity=1)

    # nut (big)
    Component.objects.create(
        product=cable,
        item=items.filter(title="Гайка М16х1,5 низька").first(),
        quantity=1)

    # special hub
    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Ковпачок (держатель)",
            part_number="Г4").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Штуцер",
            part_number="Г4").first(),
        quantity=1)

    # rod
    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Пруток",
            part_number="Г4").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Муфта",
            part_number="Г-003/002").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Кільце",
            part_number="Г-005").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Штифт",
            part_number="Г-004").first(),
        quantity=1)


def create_H2_cable(
    core_id,
    conduit_id,
    is_steel_rod_E,
    with_01,
    length
):

    items = Item.objects.all()
    notes = ""

    if is_steel_rod_E:
        notes = "Пруток 40303-Ест (чорна сталь)"

    cable_part_number = "100.М4(35)Г2.{:0>5}".format(length)
    if with_01:
        "".join(cable_part_number, "-01")

    cable = Product.objects.create(
        title="Трос Г4 (МТЗ)",
        part_number=cable_part_number,
        notes=notes)

    base_for_H_cables(cable, is_steel_rod_E)

    # # core
    # Component.objects.create(
    #     product=cable,
    #     item=items.filter(pk=core_id).first(),
    #     quantity=(length - ___ + cutting))

    # # conduit
    # Component.objects.create(
    #     product=cable,
    #     item=items.filter(pk=int(conduit_id)).first(),
    #     quantity=(length - ___ + cutting))

    # nut (small)
    Component.objects.create(
        product=cable,
        item=items.filter(title="Гайка М6").first(),
        quantity=2)

    # nut (big)
    Component.objects.create(
        product=cable,
        item=items.filter(title="Гайка М16х1,5 низька").first(),
        quantity=1)

    # hub
    Component.objects.create(
        product=cable,
        item=items.filter(part_number="40023-03").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(part_number="100.М4СБ").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(part_number="І58").first(),
        quantity=1)

    # rod
    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Пруток",
            part_number="Г203").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Муфта",
            part_number="Г-003/002" if with_01 else "Г-003/001").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Кільце",
            part_number="Г-005").first(),
        quantity=1)

    Component.objects.create(
        product=cable,
        item=items.filter(
            title="Штифт",
            part_number="Г-004/001" if with_01 else "Г-004").first(),
        quantity=1)
