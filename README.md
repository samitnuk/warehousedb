### General description

The general purpose of this project is an accounting of items in a warehouse.
This can be done manually (separately for each needed item) or automatically (through confirmation that the order is ready).

Short description of all Models used here:
- __Item__ - describes separate the *item* in a warehouse (title, part number etc.).
- __Category__ - describes separate category. Each *item* should be related to some *category*. *Category* can be marked as *special*.
This is useful when we want create *category* for some special case.
- __Product__ - describes the separate *product* in the warehouse. Generally, the *product* represents set of components.
- __Component__ - describes *component* and quantity of this *component* in the separate *product*.
Each *component* relates to some *product* and to at least one *item*.
- __Order__ - describes separate *order*. Each *order* relates to some *product*.
When we create *order* and then confirm that this *order* is ready - then will be created needed __ItemChange__ instances (see in items/signals.py).
- __ItemChange__ - describes each change in quantity for the specific *item*.
Each *itemchange* relates to some *item* and to some *order* (if *itemchange* was created automatically).
When we create *itemchange* manually with positive quantity (means we add some item to warehouse) we can choose material and related __MaterialChange__ be created automatically (if item.rate is not 0) - (see in items/signals.py).
- __Material__ - describes the separate *material* in the warehouse (title, etc.).
- __MaterialChange__ - describes each change in quantity for specific *material*.
Each *materialchange* relates to some *material* and to some *itemchange* (if *materialchange* was created automatically).
- __Tool__ - describes separate *tool* in a warehouse (title, etc.).
- __ToolChange__ - describes each change in quantity for a specific *tool*.

The quantity of *item* (or *material*, or *tool*) we can find through current_total property.

___
I included another app here [talk_keeper](https://github.com/samitnuk/talks_keeper).
Maybe here this app more updated than in the separate repo. Link to this app from any warehousedb page user will have if he in "Talkers" group.
Because of this, group "Talkers" should be created before you will go to the main page.
Probably this is not a very good decision but it's working.
