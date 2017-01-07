### General description

General purpose of this project is accounting of items in warehouse.
This can be done manualy (separate for each needed item) or automaticaly (through confirmation that order is ready).

Short description of all Models used here:
- __Item__ - describes separate *item* in warehouse (title, part number etc.).
- __Category__ - describes separate category. Each *item* should be related to some *category*. *Category* can be marked as *special*. This is useful when we want create *category* for some special case.
- __Product__ - describes separate *product* in warehouse. Generally, *product* represents set of components.
- __Component__ - describes *component* and quantity of this *component* in separate *product*. Each *component* relates to some *product* and to at least one *item*.
- __Order__ - describes separate *order*. Each *order* relates to some one *product*. When we create *order* and then confim that this *order* is ready - then will be created needed __ItemChange__ instances (see in items/signals.py).
- __ItemChange__ - describes each change in quantity for specific *item*. Each *itemchange* relates to some *item* and to some *order* (if *itemchange* was created automaticaly). When we create *itemchange* manualy with positive quantity (means we add some item to warehouse) we can chose material and related __MaterialChange__ be created automaticaly (if item.rate is not 0) - (see in items/signals.py).
- __Material__ - describes separate *material* in warehouse (title, etc.).
- __MaterialChange__ - describes each change in quantity for specific *material*. Each *materialchange* relates to some *material* and to some *itemchange* (if *materialchange* was created automaticaly).
- __Tool__ - describes separate *tool* in warehouse (title, etc.).
- __ToolChange__ - describes each change in quantity for specific *tool*.

Quantity of *item* (or *material*, or *tool*) we can find through current_total property.
