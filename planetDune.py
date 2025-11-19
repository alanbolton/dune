
DuneSector0 = [ ('Polar_Sink_0',2)]
DuneSector1 = [('Cielago_North_1',1), ('Meridian_1',1), ('Cielago_West_1',1), ('Cielago_Depression_1',1)]
DuneSector2 = [('Cielago_North_2',1), ('Cielago_South_2',1),('Meridian_2',1),('Cielago_Depression_2',1)]
DuneSector3 = [('Cielago_North_3',1), ('Cielago_South_3',1), ('Cielago_East_3',1),('Cielago_Depression_3',1)]
DuneSector4 = [('False_Wall_South_4',2), ('South_Mesa_4',1), ('Cielago_East_4',1),('Harg_Pass_4',1)]
DuneSector5 = [('False_Wall_South_5',2), ('South_Mesa_5',1), ('Pasty_Mesa_5',2), ('Harg_Pass_5',1), ('False_Wall_East_5',1), ('The_Minor_Erg_5',1), ('Tueks_Sietch_5',3)]
DuneSector6 = [('Pasty_Mesa_6',2), ('South_Mesa_6',1), ('False_Wall_East_6',1), ('The_Minor_Erg_6',1)]
DuneSector7 = [('Pasty_Mesa_7',2), ('Red_Chasm_7',1),('False_Wall_East_7',1), ('The_Minor_Erg_7',1)]
DuneSector8 = [('Pasty_Mesa_8',2), ('Gara_Kulon_8',1),  ('False_Wall_East_8',1),('Sheild_Wall_8',2), ('The_Minor_Erg_8',1)]
DuneSector9 = [('Imperial_Basin_9',1), ('OH_Gap_9',1), ('False_Wall_East_9',1),('Sheild_Wall_9',2), ('Hole_in_the_Rock_9',1), ('Sihaya_Ridge_9',1), ('Rim_Wall_West_9',2), ('Basin_9',1)]
DuneSector10 = [('Imperial_Basin_10',1), ('OH_Gap_10',1), ('Arrakeen_10',3)]
DuneSector11 = [('Imperial_Basin_11',1), ('OH_Gap_11',1), ('Broken_Land_11',1), ('Tsimpo_11',1), ('Arsunt_11',1), ('Carthag_11',3)]
DuneSector12 = [('Plastic_Basin_12',2), ('Hagga_Basin_12',1), ('Broken_Land_12',1), ('Tsimpo_12',1), ('Arsunt_12',1)]
DuneSector13 = [('Plastic_Basin_13',2), ('Hagga_Basin_13',1), ('Rock_Outcroppings_13',1), ('Tsimpo_13',1)]
DuneSector14 = [('Plastic_Basin_14',2), ('Wind_Pass_14',1), ('Rock_Outcroppings_14',1), ('Bight_of_the_Cliff_14',1), ('Sietch_Tabr_14',3)]
DuneSector15 = [('Funeral_Plain_15',1), ('Wind_Pass_15',1), ('The_Great_Flat_15',1), ('Bight_of_the_Cliff_15',1)]
DuneSector16 = [('False_Wall_West_16',2), ('Wind_Pass_16',1), ('Habbanya_Erg_16',1), ('The_Greater_Flat_16',1)]
DuneSector17 = [('False_Wall_West_17',2), ('Wind_Pass_17',1), ('Wind_Pass_North_17',1), ('Habbanya_Erg_17',1), ('Habbanya_Ridge_Flat_17',1), ('Habbanya_Ridge_Sietch_17',3)]
DuneSector18 = [('False_Wall_West_18',2), ('Cielago_West_18',1),('Wind_Pass_North_18',1), ('Habbanya_Ridge_Flat_18',1)]


PolarSink_0 = [('Cielago_North_1',1), ('Cielago_North_2',1), ('Cielago_North_3',1), ('Harg_Pass_4',1), ('False_Wall_East_5',1), \
              ('False_Wall_East_6',1), ('False_Wall_East_7',1), ('False_Wall_East_8',1), ('False_Wall_East_9',1), \
              ('Imperial_Basin_9',1),  ('Imperial_Basin_10',1), ('Imperial_Basin_11',1), ('Arsunt_11',1), ('Arsunt_12',1), \
              ('Hagga_Basin_13',1), ('Wind_Pass_14',1), ('Wind_Pass_15',1), ('Wind_Pass_16',1),  ('Wind_Pass_North_17',1),
              ('Wind_Pass_North_18',1)]
Meridian_1 = [('Meridian_2', 0), ('Cielago_Depression_1', 1), ('Cielago_West_1', 1),  ('Habbanya_Ridge_Flat_18', 1)]
Cielago_Depression_1 = [('Cielago_Depression_2', 0), ('Meridian_1', 1), ('Cielago_West_1', 1),  ('Cielago_North_1', 1)]
Cielago_West_1 = [('Cielago_West_18',0), ('Cielago_Depression_1', 1), ('Meridian_1', 1),  ('Cielago_North_1', 1)]
Cielago_North_1 = [('Cielago_North_2',0), ('Wind_Pass_North_18', 1), ('Cielago_West_18', 1),  ('Cielago_West_1', 1), \
                    ('Cielago_Depression_1', 1), ('Polar_Sink_0',1)]
Cielago_North_2 = [('Cielago_North_1',0), ('Cielago_North_3',0), ('Cielago_Depression_2', 1), ('Polar_Sink_0',1)]
Cielago_Depression_2 = [('Cielago_Depression_1', 0), ('Cielago_Depression_3', 0), ('Cielago_North_2', 1), ('Meridian_2', 1), \
                        ('Cielago_South_2', 1)]
Meridian_2 =  [('Meridian_1', 0), ('Cielago_Depression_2', 1), ('Cielago_South_2', 1)]
Cielago_South_2 = [('Cielago_South_3', 0), ('Cielago_Depression_2', 1), ('Meridian_2', 1)]
Cielago_South_3 = [('Cielago_South_2', 0), ('Cielago_Depression_3', 1), ('Cielago_East_3', 1)]
Cielago_East_3 =  [('Cielago_East_4', 0), ('Cielago_Depression_3', 1), ('False_Wall_South_4', 1), ('Cielago_North_3',1),\
                   ('Cielago_South_3', 1)]
Cielago_Depression_3 =[('Cielago_Depression_2', 0), ('Cielago_East_3', 1), ('Cielago_South_3', 1), ('Cielago_North_3',1)]
Cielago_North_3 = [('Cielago_North_2', 0), ('Harg_Pass_4',1), ('False_Wall_South_4', 1), ('Cielago_East_3', 1),\
                   ('Cielago_Depression_3', 1), ('Polar_Sink_0',1)]
Cielago_East_4 = [('Cielago_East_3', 0), ('South_Mesa_4', 1), ('False_Wall_South_4', 1)]
South_Mesa_4 = [('South_Mesa_5', 0), ('Cielago_East_4', 1), ('False_Wall_South_4', 1)]
False_Wall_South_4 = [('False_Wall_South_5', 0), ('Cielago_East_4', 1), ('South_Mesa_4', 1), ('Harg_Pass_4',1), ('Cielago_North_3', 1)]
Harg_Pass_4 = [('Harg_Pass_5',0), ('False_Wall_East_5',1), ('False_Wall_South_4', 1), ('Polar_Sink_0',1)]
South_Mesa_5 = [('South_Mesa_4', 0), ('South_Mesa_6', 0), ('Tueks_Sietch_5', 1), ('False_Wall_South_5', 1), ('Pasty_Mesa_5', 1)]
Tueks_Sietch_5 = [('South_Mesa_5', 1), ('False_Wall_South_5', 1),  ('Pasty_Mesa_5', 1)]
False_Wall_South_5 = [('False_Wall_South_4', 0), ('Pasty_Mesa_5', 1), ('South_Mesa_5', 1), ('Harg_Pass_5',1),\
                      ('The_Minor_Erg_5',1), ('Tueks_Sietch_5', 1)]
Pasty_Mesa_5 = [('Pasty_Mesa_6', 0), ('Tueks_Sietch_5', 1), ('South_Mesa_5', 1), ('False_Wall_South_5',1), ('The_Minor_Erg_5',1)]
The_Minor_Erg_5 = [('The_Minor_Erg_6', 0), ('Harg_Pass_5', 1), ('False_Wall_East_5', 1), ('False_Wall_South_5',1), ('Pasty_Mesa_5',1)]
Harg_Pass_5 = [('Harg_Pass_4',0), ('False_Wall_East_5',1), ('The_Minor_Erg_5', 1), ('False_Wall_South_5',1)]
False_Wall_East_5 = [('False_Wall_East_6',0), ('The_Minor_Erg_5',1), ('Harg_Pass_5', 1),  ('Polar_Sink_0',1)]
False_Wall_East_6 = [('False_Wall_East_5',0), ('False_Wall_East_7',0), ('The_Minor_Erg_6',1), ('Polar_Sink_0',1)]
The_Minor_Erg_6 = [('The_Minor_Erg_5', 0), ('The_Minor_Erg_7', 0), ('False_Wall_East_6', 1), ('Pasty_Mesa_6',1)]
Pasty_Mesa_6 = [('Pasty_Mesa_5', 0), ('Pasty_Mesa_7', 0), ('The_Minor_Erg_6', 1), ('South_Mesa_6', 1)]
South_Mesa_6 = [('South_Mesa_5', 0), ('Red_Chasm_7', 1), ('Pasty_Mesa_6', 1)]
False_Wall_East_7 = [('False_Wall_East_6',0), ('False_Wall_East_8',0), ('The_Minor_Erg_7',1), ('Polar_Sink_0',1)]
The_Minor_Erg_7 = [('The_Minor_Erg_6', 0), ('The_Minor_Erg_8', 0), ('False_Wall_East_7', 1), ('Pasty_Mesa_7',1)]
Pasty_Mesa_7 = [('Pasty_Mesa_6', 0), ('Pasty_Mesa_8', 0), ('Red_Chasm_7', 1), ('The_Minor_Erg_7', 1)]
Red_Chasm_7 = [('Pasty_Mesa_7', 1), ('South_Mesa_6', 1)]
False_Wall_East_8 = [('False_Wall_East_7',0), ('False_Wall_East_9',1), ('The_Minor_Erg_8',1), ('Sheild_Wall_8', 1), \
                     ('Polar_Sink_0',1)]
The_Minor_Erg_8 = [('The_Minor_Erg_7', 0), ('False_Wall_East_8', 1),('Sheild_Wall_8', 1), ('Pasty_Mesa_8',1)]
Pasty_Mesa_8 = [('Pasty_Mesa_7', 0), ('Sheild_Wall_8', 1), ('Gara_Kulon_8', 1), ('The_Minor_Erg_8', 1)]
Sheild_Wall_8 = [('Sheild_Wall_9',0), ('The_Minor_Erg_8',1), ('Gara_Kulon_8',1), ('False_Wall_East_8',1)]
Gara_Kulon_8 = [('Sheild_Wall_8', 1), ('Pasty_Mesa_8', 1), ('Sihaya_Ridge_9', 1)]
False_Wall_East_9 = [('False_Wall_East_8', 0), ('Sheild_Wall_9', 1), ('Imperial_Basin_9', 1), ('Polar_Sink_0', 1)]
Sheild_Wall_9 = [('Sheild_Wall_8', 0), ('Imperial_Basin_9', 1), ('False_Wall_East_9', 1), ('Hole_in_the_Rock_9', 1),\
                 ('Sihaya_Ridge_9', 1)]
Imperial_Basin_9 = [('Imperial_Basin_10', 0), ('False_Wall_East_9', 1), ('Sheild_Wall_9', 1), ('Hole_in_the_Rock_9', 1), \
                    ('Rim_Wall_West_9', 1), ('Polar_Sink_0', 1)]
Hole_in_the_Rock_9 = [('Imperial_Basin_9', 1), ('Sheild_Wall_9', 1), ('Rim_Wall_West_9', 1), ('Sihaya_Ridge_9', 1),('Basin_9', 1)]
Rim_Wall_West_9 = [('Imperial_Basin_9', 1), ('Imperial_Basin_10', 1), ('Hole_in_the_Rock_9', 1),  ('Basin_9', 1),\
                   ('OH_Gap_9', 1), ('OH_Gap_10', 1), ('Arrakeen_10', 1)]
Basin_9 = [('OH_Gap_9', 1), ('Sihaya_Ridge_9', 1), ('Rim_Wall_West_9', 1),  ('Hole_in_the_Rock_9', 1)]
OH_Gap_9 = [('OH_Gap_10', 0), ('Rim_Wall_West_9', 1), ('Basin_9', 1)]
Sihaya_Ridge_9 = [('Gara_Kulon_8', 1), ('Sheild_Wall_9', 1), ('Hole_in_the_Rock_9', 1), ('Basin_9', 1)]
Imperial_Basin_10 = [('Imperial_Basin_9', 0), ('Imperial_Basin_11', 0), ('Rim_Wall_West_9', 1), ('Arrakeen_10', 1), \
                     ('OH_Gap_10', 1), ('Arsunt_11', 1), ('Polar_Sink_0', 1)]
OH_Gap_10 = [('OH_Gap_9', 0), ('OH_Gap_11', 0), ('Arrakeen_10', 1), ('Imperial_Basin_10', 1)]
Arrakeen_10 = [('OH_Gap_10', 1), ('Rim_Wall_West_9', 1), ('Imperial_Basin_10', 1)]
Imperial_Basin_11 = [('Imperial_Basin_10', 0), ('Arsunt_11', 1), ('Carthag_11', 1), ('Tsimpo_11', 1)]
Arsunt_11 = [('Arsunt_12', 0),('Imperial_Basin_10', 1), ('Imperial_Basin_11', 1), ('Hagga_Basin_12', 1), ('Carthag_11', 1),\
              ('Polar_Sink_0', 1)]
Carthag_11 = [('Arsunt_11', 1), ('Imperial_Basin_11', 1), ('Tsimpo_11', 1), ('Tsimpo_12', 1), ('Hagga_Basin_12', 1)]
Tsimpo_11 = [('Tsimpo_12', 0), ('OH_Gap_11', 1),('Carthag_11', 1), ('Imperial_Basin_11', 1), ('Broken_Land_11', 1)]
OH_Gap_11 = [('OH_Gap_10', 0), ('Broken_Land_11', 1),('Tsimpo_11', 1)]
Broken_Land_11 = [('Broken_Land_12', 0), ('Tsimpo_11', 1), ('OH_Gap_11', 1)]
Arsunt_12 = [('Arsunt_11', 0),('Hagga_Basin_12', 1), ('Polar_Sink_0', 1)]
Hagga_Basin_12 = [('Hagga_Basin_13', 0), ('Arsunt_11', 1), ('Arsunt_12', 1), ('Carthag_11', 1), ('Tsimpo_12', 1)]
Tsimpo_12 = [('Tsimpo_11', 0), ('Tsimpo_13', 0), ('Broken_Land_12', 1), ('Carthag_11', 1), ('Hagga_Basin_12', 1), \
             ('Plastic_Basin_12', 1)]
Broken_Land_12 = [('Broken_Land_11', 0), ('Tsimpo_12', 1), ('Plastic_Basin_12', 1), ('Rock_Outcroppings_13', 1)]
Plastic_Basin_12 = [('Plastic_Basin_13', 0), ('Broken_Land_12', 1), ('Tsimpo_12', 1)]
Hagga_Basin_13 = [('Hagga_Basin_12', 0), ('Arsunt_12', 1), ('Wind_Pass_14', 1), ('Plastic_Basin_12', 1), ('Plastic_Basin_13', 1), \
                  ('Tsimpo_13',1), ('Polar_Sink_0', 1)]
Plastic_Basin_13 = [('Plastic_Basin_12', 0), ('Plastic_Basin_14', 0), ('Hagga_Basin_13', 1), ('Tsimpo_13', 1), \
                    ('Rock_Outcroppings_13', 1)]
Tsimpo_13 = [('Tsimpo_12', 0), ('Hagga_Basin_13', 1), ('Plastic_Basin_13', 1)]
Rock_Outcroppings_13 = [('Rock_Outcroppings_14', 0), ('Broken_Land_12', 1), ('Plastic_Basin_13', 1)]
Wind_Pass_14 = [('Wind_Pass_15', 0), ('Hagga_Basin_13', 1), ('Plastic_Basin_14', 1), ('Polar_Sink_0', 1)]
Plastic_Basin_14 = [('Plastic_Basin_13', 0), ('Wind_Pass_14', 1), ('Hagga_Basin_13', 1), ('Sietch_Tabr_14', 1), \
                    ('Rock_Outcroppings_14', 1), ('Bight_of_the_Cliff_14', 1), ('Funeral_Plain_15', 1),  ('The_Great_Flat_15', 1)]
Bight_of_the_Cliff_14 = [('Bight_of_the_Cliff_15', 0), ('Plastic_Basin_14', 1), ('Sietch_Tabr_14', 1),  ('Rock_Outcroppings_14', 1)]
Rock_Outcroppings_14 = [('Rock_Outcroppings_13', 0), ('Bight_of_the_Cliff_14', 1), ('Plastic_Basin_14', 1),  ('Sietch_Tabr_14', 1)]
Sietch_Tabr_14 = [('Rock_Outcroppings_14', 1), ('Bight_of_the_Cliff_14', 1), ('Plastic_Basin_14', 1)]
Wind_Pass_15 = [('Wind_Pass_14', 0), ('Wind_Pass_16', 0), ('The_Great_Flat_15', 1), ('Polar_Sink_0', 1)]
The_Great_Flat_15 = [('Wind_Pass_15', 1), ('Plastic_Basin_14', 1), ('Funeral_Plain_15', 1), ('The_Greater_Flat_16', 1)]
Funeral_Plain_15 = [('The_Great_Flat_15', 1), ('Plastic_Basin_14', 1), ('Bight_of_the_Cliff_15', 1)]
Bight_of_the_Cliff_15 = [('Bight_of_the_Cliff_14', 0), ('Funeral_Plain_15', 1)]
Wind_Pass_16 = [('Wind_Pass_15', 0), ('Wind_Pass_17', 0), ('Wind_Pass_North_17', 0), ('The_Greater_Flat_16', 1), \
                ('False_Wall_West_16', 1), ('Polar_Sink_0', 1)]
False_Wall_West_16 = [('False_Wall_West_17', 0), ('Wind_Pass_16', 1), ('The_Greater_Flat_16', 1), ('Habbanya_Erg_16', 1)]
The_Greater_Flat_16 = [('Wind_Pass_16', 1), ('False_Wall_West_16', 1), ('The_Great_Flat_15', 1), ('Habbanya_Erg_16', 1)]
Habbanya_Erg_16 = [('Habbanya_Erg_17', 0), ('The_Greater_Flat_16', 1), ('Habbanya_Ridge_Flat_17', 1), ('False_Wall_West_16', 1)]
Wind_Pass_North_17 = [('Wind_Pass_North_18', 0), ('Wind_Pass_16', 1), ('Wind_Pass_17', 1), ('Polar_Sink_0', 1)]
Wind_Pass_17 = [('Wind_Pass_16', 0), ('Wind_Pass_North_17', 1), ('False_Wall_West_17', 1), ('Cielago_West_18', 1)]
False_Wall_West_17 = [('False_Wall_West_16', 0), ('False_Wall_West_18', 0), ('Wind_Pass_17', 1), ('Habbanya_Erg_17', 1),\
                      ('Habbanya_Ridge_Flat_17', 1)]
Habbanya_Erg_17 = [('Habbanya_Erg_16', 0), ('False_Wall_West_17', 1), ('Habbanya_Ridge_Flat_17', 1)]
Habbanya_Ridge_Flat_17 = [('Habbanya_Ridge_Flat_18', 0), ('Habbanya_Erg_17', 1), ('Habbanya_Erg_16', 1), \
                          ('False_Wall_West_17', 1), ('Habbanya_Ridge_Sietch_17', 1)]
Habbanya_Ridge_Sietch_17 = [('Habbanya_Ridge_Flat_17', 1), ('Habbanya_Ridge_Flat_18', 1)]
Wind_Pass_North_18 = [('Wind_Pass_North_17', 0), ('Cielago_North_1', 1), ('Cielago_West_18', 1), ('Polar_Sink_0', 1)]
Cielago_West_18 = [('Cielago_West_1', 0), ('Cielago_North_1', 1), ('Wind_Pass_17', 1), ('Wind_Pass_North_18', 1), \
                   ('False_Wall_West_18', 1), ('Habbanya_Ridge_Flat_18',1)]
False_Wall_West_18 = [('False_Wall_West_17', 0), ('Cielago_West_18', 1), ('Habbanya_Ridge_Flat_18',1)]
Habbanya_Ridge_Flat_18 = [('Habbanya_Ridge_Flat_17', 0), ('Meridian_1', 1), ('Cielago_West_18', 1), ('False_Wall_West_18', 1), \
                          ('Habbanya_Ridge_Sietch_17', 1)]

def territories_by_sector_get(sector):
    sector_management = {
        0: DuneSector0 ,
        1: DuneSector1 ,
        2: DuneSector2,
        3: DuneSector3,
        4: DuneSector4,
        5: DuneSector5,
        6: DuneSector6,
        7: DuneSector7,
        8: DuneSector8,
        9: DuneSector9,
        10: DuneSector10 ,
        11: DuneSector11 ,
        12: DuneSector12,
        13: DuneSector13,
        14: DuneSector14,
        15: DuneSector15,
        16: DuneSector16,
        17: DuneSector17,
        18: DuneSector18,
    }
    return sector_management.get(sector, lambda: DuneSector0)

def territories_neighbors_get(territory):
    neighbor_management = {
        'Polar_Sink_0': PolarSink_0,
        'Meridian_1': Meridian_1,
        'Cielago_Depression_1': Cielago_Depression_1,
        'Cielago_West_1': Cielago_West_1,
        'Cielago_North_1': Cielago_North_1,
        'Cielago_North_2': Cielago_North_2,
        'Cielago_Depression_2': Cielago_Depression_2,
        'Meridian_2': Meridian_2,
        'Cielago_South_2': Cielago_South_2,
        'Cielago_South_3': Cielago_South_3,
        'Cielago_East_3': Cielago_East_3 ,
        "Cielago_Depression_3": Cielago_Depression_3 ,
        'Cielago_North_3': Cielago_North_3,
        'Cielago_East_4': Cielago_East_4,
        'South_Mesa_4': South_Mesa_4,
        'False_Wall_South_4': False_Wall_South_4,
        'Harg_Pass_4': Harg_Pass_4,
        'South_Mesa_5': South_Mesa_5,
        'Tueks_Sietch_5': Tueks_Sietch_5,
        'False_Wall_South_5': False_Wall_South_5,
        'Pasty_Mesa_5': Pasty_Mesa_5,
        'The_Minor_Erg_5': The_Minor_Erg_5,
        'Harg_Pass_5': Harg_Pass_5,
        'False_Wall_East_5': False_Wall_East_5,
        'False_Wall_East_6': False_Wall_East_6,
        'The_Minor_Erg_6': The_Minor_Erg_6,
        'Pasty_Mesa_6': Pasty_Mesa_6,
        'South_Mesa_6': South_Mesa_6,
        'False_Wall_East_7': False_Wall_East_7,
        'The_Minor_Erg_7': The_Minor_Erg_7,
        'Pasty_Mesa_7': Pasty_Mesa_7,
        'Red_Chasm_7': Red_Chasm_7,
        'False_Wall_East_8': False_Wall_East_8,
        'The_Minor_Erg_8': The_Minor_Erg_8,
        'Pasty_Mesa_8': Pasty_Mesa_8,
        'Sheild_Wall_8': Sheild_Wall_8,
        'Gara_Kulon_8': Gara_Kulon_8,
        'False_Wall_East_9': False_Wall_East_9,
        'Sheild_Wall_9': Sheild_Wall_9,
        'Imperial_Basin_9': Imperial_Basin_9,
        'Hole_in_the_Rock_9': Hole_in_the_Rock_9,
        'Rim_Wall_West_9': Rim_Wall_West_9,
        'Basin_9': Basin_9,
        'OH_Gap_9': OH_Gap_9,
        'Sihaya_Ridge_9': Sihaya_Ridge_9,
        'Imperial_Basin_10': Imperial_Basin_10,
        'OH_Gap_10': OH_Gap_10,
        'Arrakeen_10': Arrakeen_10,
        'Imperial_Basin_11': Imperial_Basin_11,
        'Arsunt_11': Arsunt_11,
        'Carthag_11': Carthag_11,
        'Tsimpo_11': Tsimpo_11,
        'OH_Gap_11': OH_Gap_11,
        'Broken_Land_11': Broken_Land_11,
        'Arsunt_12': Arsunt_12,
        'Hagga_Basin_12': Hagga_Basin_12,
        'Tsimpo_12': Tsimpo_12,
        'Broken_Land_12': Broken_Land_12,
        'Plastic_Basin_12': Plastic_Basin_12,
        'Hagga_Basin_13': Hagga_Basin_13,
        'Plastic_Basin_13': Plastic_Basin_13,
        'Tsimpo_13': Tsimpo_13,
        'Rock_Outcroppings_13': Rock_Outcroppings_13,
        'Wind_Pass_14': Wind_Pass_14,
        'Plastic_Basin_14': Plastic_Basin_14,
        'Bight_of_the_Cliff_14': Bight_of_the_Cliff_14,
        'Rock_Outcroppings_14': Rock_Outcroppings_14,
        'Sietch_Tabr_14': Sietch_Tabr_14,
        'Wind_Pass_15': Wind_Pass_15,
        'The_Great_Flat_15': The_Great_Flat_15,
        'Funeral_Plain_15': Funeral_Plain_15,
        'Bight_of_the_Cliff_15': Bight_of_the_Cliff_15,
        'Wind_Pass_16': Wind_Pass_16,
        'False_Wall_West_16': False_Wall_West_16,
        'The_Greater_Flat_16': The_Greater_Flat_16,
        'Habbanya_Erg_16': Habbanya_Erg_16,
        'Wind_Pass_North_17': Wind_Pass_North_17,
        'Wind_Pass_17': Wind_Pass_17,
        'False_Wall_West_17': False_Wall_West_17,
        'Habbanya_Erg_17': Habbanya_Erg_17,
        'Habbanya_Ridge_Flat_17': Habbanya_Ridge_Flat_17,
        'Habbanya_Ridge_Sietch_17': Habbanya_Ridge_Sietch_17,
        'Wind_Pass_North_18': Wind_Pass_North_18,
        'Cielago_West_18': Cielago_West_18,
        'False_Wall_West_18': False_Wall_West_18,
        'Habbanya_Ridge_Flat_18': Habbanya_Ridge_Flat_18
    }
    return neighbor_management.get(territory, lambda: DuneSector0)

PolarSink = ['PolarSink_0']
Meridian = ['Meridian_1','Meridian_2']
Cielago_Depression = ['Cielago_Depression_1','Cielago_Depression_2','Cielago_Depression_3']
Cielago_West = ['Cielago_West_1','Cielago_West_18']
Cielago_North = ['Cielago_North_1','Cielago_North_2','Cielago_North_3']
Cielago_South = ['Cielago_South_2','Cielago_South_3']
Cielago_East =  ['Cielago_East_3','Cielago_East_4']
South_Mesa = ['South_Mesa_4','South_Mesa_5','South_Mesa_6']
False_Wall_South = ['False_Wall_South_4', 'False_Wall_South_5']
Harg_Pass = ['Harg_Pass_4', 'Harg_Pass_5']
Tueks_Sietch = ['Tueks_Sietch_5']
Pasty_Mesa = ['Pasty_Mesa_5', 'Pasty_Mesa_6','Pasty_Mesa_7','Pasty_Mesa_8']
The_Minor_Erg = ['The_Minor_Erg_5', 'The_Minor_Erg_6','The_Minor_Erg_7','The_Minor_Erg_8',]
False_Wall_East = ['False_Wall_East_5','False_Wall_East_6', 'False_Wall_East_7', 'False_Wall_East_8', 'False_Wall_East_9' ]
Red_Chasm = ['Red_Chasm_7']
Sheild_Wall = ['Sheild_Wall_8', 'Sheild_Wall_9']
Gara_Kulon = ['Gara_Kulon_8']
Imperial_Basin = ['Imperial_Basin_9','Imperial_Basin_10', 'Imperial_Basin_11',]
Hole_in_the_Rock = ['Hole_in_the_Rock_9']
Rim_Wall_West = ['Rim_Wall_West_9']
Basin = ['Basin_9']
OH_Gap = ['OH_Gap_9','OH_Gap_10', 'OH_Gap_11']
Sihaya_Ridge = ['Sihaya_Ridge_9']
Arrakeen = ['Arrakeen_10']
Arsunt = ['Arsunt_11', 'Arsunt_12']
Carthag = ['Carthag_11']
Tsimpo = ['Tsimpo_11', 'Tsimpo_12', 'Tsimpo_13']
Broken_Land = ['Broken_Land_11', 'Broken_Land_12']
Hagga_Basin = ['Hagga_Basin_12', 'Hagga_Basin_13']
Plastic_Basin = ['Plastic_Basin_12', 'Plastic_Basin_13', 'Plastic_Basin_14']
Rock_Outcroppings = ['Rock_Outcroppings_13', 'Rock_Outcroppings_14']
Wind_Pass = ['Wind_Pass_14', 'Wind_Pass_15', 'Wind_Pass_16', 'Wind_Pass_17']
Bight_of_the_Cliff = ['Bight_of_the_Cliff_14', 'Bight_of_the_Cliff_15']
Sietch_Tabr = ['Sietch_Tabr_14']
The_Great_Flat = ['The_Great_Flat_15']
Funeral_Plain = ['Funeral_Plain_15']
False_Wall_West = ['False_Wall_West_16', 'False_Wall_West_17', 'False_Wall_West_18']
The_Greater_Flat = ['The_Greater_Flat_16']
Habbanya_Erg = ['Habbanya_Erg_16', 'Habbanya_Erg_17']
Wind_Pass_North = ['Wind_Pass_North_17', 'Wind_Pass_North_18']
Habbanya_Ridge_Flat = ['Habbanya_Ridge_Flat_17', 'Habbanya_Ridge_Flat_18']
Habbanya_Ridge_Sietch = ['Habbanya_Ridge_Sietch_17']

def territories_aliases_get(territory):
    aliases = {
        'Arrakeen_10': Arrakeen,
        'Arsunt_11': Arsunt,
        'Arsunt_12': Arsunt,
        'Basin_9': Basin,
        'Bight_of_the_Cliff_14': Bight_of_the_Cliff,
        'Bight_of_the_Cliff_15': Bight_of_the_Cliff,
        'Broken_Land_11': Broken_Land,
        'Broken_Land_12': Broken_Land,
        'Cielago_Depression_1': Cielago_Depression,
        'Cielago_Depression_2': Cielago_Depression,
        'Cielago_Depression_3': Cielago_Depression ,
        'Cielago_West_1': Cielago_West,
        'Cielago_West_18': Cielago_West,
        'Cielago_North_1': Cielago_North,
        'Cielago_North_2': Cielago_North,
        'Cielago_North_3': Cielago_North,
        'Cielago_South_2': Cielago_South,
        'Cielago_South_3': Cielago_South,
        'Cielago_East_3': Cielago_East ,
        'Cielago_East_4': Cielago_East,
        'Carthag_11': Carthag,
        'False_Wall_East_5': False_Wall_East,
        'False_Wall_East_6': False_Wall_East,
        'False_Wall_East_7': False_Wall_East,
        'False_Wall_East_8': False_Wall_East,
        'False_Wall_East_9': False_Wall_East,
        'False_Wall_South_4': False_Wall_South,
        'False_Wall_South_5': False_Wall_South,
        'Funeral_Plain_15': Funeral_Plain,
        'False_Wall_West_16': False_Wall_West,
        'False_Wall_West_17': False_Wall_West,
        'False_Wall_West_18': False_Wall_West,
        'Gara_Kulon_8': Gara_Kulon,
        'Habbanya_Erg_16': Habbanya_Erg,
        'Habbanya_Erg_17': Habbanya_Erg,
        'Habbanya_Ridge_Flat_17': Habbanya_Ridge_Flat,
        'Habbanya_Ridge_Flat_18': Habbanya_Ridge_Flat,
        'Habbanya_Ridge_Sietch_17': Habbanya_Ridge_Sietch,
        'Hagga_Basin_12': Hagga_Basin,
        'Hagga_Basin_13': Hagga_Basin,
        'Harg_Pass_4': Harg_Pass,
        'Harg_Pass_5': Harg_Pass,
        'Hole_in_the_Rock_9': Hole_in_the_Rock,
        'Imperial_Basin_9': Imperial_Basin,
        'Imperial_Basin_10': Imperial_Basin,
        'Imperial_Basin_11': Imperial_Basin,
        'Meridian_1': Meridian,
        'Meridian_2': Meridian,
        'OH_Gap_9': OH_Gap,
        'OH_Gap_10': OH_Gap,
        'OH_Gap_11': OH_Gap,
        'Pasty_Mesa_5': Pasty_Mesa,
        'Pasty_Mesa_6': Pasty_Mesa,
        'Pasty_Mesa_7': Pasty_Mesa,
        'Pasty_Mesa_8': Pasty_Mesa,
        'Plastic_Basin_12': Plastic_Basin,
        'Plastic_Basin_13': Plastic_Basin,
        'Plastic_Basin_14': Plastic_Basin,
        'Polar_Sink_0': PolarSink,
        'Red_Chasm_7': Red_Chasm,
        'Rim_Wall_West_9': Rim_Wall_West,
        'Rock_Outcroppings_13': Rock_Outcroppings,
        'Rock_Outcroppings_14': Rock_Outcroppings,
        'South_Mesa_5': South_Mesa,
        'South_Mesa_6': South_Mesa,
        'South_Mesa_4': South_Mesa,
        'Sheild_Wall_8': Sheild_Wall,
        'Sheild_Wall_9': Sheild_Wall,
        'Sietch_Tabr_14': Sietch_Tabr,
        'Sihaya_Ridge_9': Sihaya_Ridge,
        'The_Great_Flat_15': The_Great_Flat,
        'The_Greater_Flat_16': The_Greater_Flat,
        'The_Minor_Erg_5': The_Minor_Erg,
        'The_Minor_Erg_6': The_Minor_Erg,
        'The_Minor_Erg_7': The_Minor_Erg,
        'The_Minor_Erg_8': The_Minor_Erg,
        'Tsimpo_11': Tsimpo,
        'Tsimpo_12': Tsimpo,
        'Tsimpo_13': Tsimpo,
        'Tueks_Sietch_5': Tueks_Sietch,
        'Wind_Pass_14': Wind_Pass,
        'Wind_Pass_15': Wind_Pass,
        'Wind_Pass_16': Wind_Pass,
        'Wind_Pass_17': Wind_Pass,
        'Wind_Pass_North_17': Wind_Pass_North,
        'Wind_Pass_North_18': Wind_Pass_North,
    }
    return aliases.get(territory, lambda: None)

No_Spice = [(0, 0)]
Cielago_South_Spice = [(415, 725)]
Cielago_North_Spice = [(430, 515)]
South_Mesa_Spice = [(710, 520)]
Red_Chasm_Spice = [(725, 365)]
The_Minor_Erg_Spice = [(520, 330)]
Sihaya_Ridge_Spice = [(645, 150)]
OH_Gap_Spice = [(495, 75)]
Broken_Land_Spice = [(320, 70)]
Hagga_Basin_Spice = [(300, 275)]
Rock_Outcroppings_Spice = [(110, 200)]
The_Great_Flat_Spice = [(125, 380)]
Funeral_Plain_Spice = [(125, 340)]
Habbanya_Erg_Spice = [(85, 485)]
Wind_Pass_North_Spice = [(325, 425)]
Habbanya_Ridge_Flat_Spice = [(155, 630)]
#
def territories_spice_marker_get(territory):
    spice_management = {
        'No_Spice': No_Spice,
        'Cielago_South_2': Cielago_South_Spice,
        'Cielago_North_3': Cielago_North_Spice,
        'South_Mesa_5': South_Mesa_Spice,
        'Red_Chasm_7': Red_Chasm_Spice,
        'The_Minor_Erg_8': The_Minor_Erg_Spice,
        'Sihaya_Ridge_9': Sihaya_Ridge_Spice,
        'OH_Gap_10': OH_Gap_Spice,
        'Broken_Land_12': Broken_Land_Spice,
        'Hagga_Basin_13': Hagga_Basin_Spice,
        'Rock_Outcroppings_14': Rock_Outcroppings_Spice,
        'The_Great_Flat_15': The_Great_Flat_Spice,
        'Funeral_Plain_15': Funeral_Plain_Spice,
        'Habbanya_Erg_16': Habbanya_Erg_Spice,
        'Wind_Pass_North_17': Wind_Pass_North_Spice,
        'Habbanya_Ridge_Flat_18': Habbanya_Ridge_Flat_Spice
    }
    return spice_management.get(territory, No_Spice)


Default_Markers = [(0,0)]
PolarSink_0_Troop_Markers = [(370, 365, 'Polar_Sink_0')]
Meridian_1_Troop_Markers = [(260, 700, 'Meridian_1')]
Cielago_Depression_1_Troop_Markers = [(310, 630, 'Cielago_Depression_1')]
Cielago_West_1_Troop_Markers = [(285, 590, 'Cielago_West_1')]
Cielago_North_1_Troop_Markers = [(320, 550, 'Cielago_North_1')]
Cielago_North_2_Troop_Markers = [(385, 555, 'Cielago_North_2')]
Cielago_Depression_2_Troop_Markers = [(385, 630, 'Cielago_Depression_2')]
Meridian_2_Troop_Markers =  [(345, 735, 'Meridian_2')]
Cielago_South_2_Troop_Markers = [(380, 660, 'Cielago_South_2')]
Cielago_South_3_Troop_Markers = [(460, 720, 'Cielago_South_3')]
Cielago_East_3_Troop_Markers =  [(495, 695,'Cielago_East_3')]
Cielago_Depression_3_Troop_Markers =[(440, 600,'Cielago_Depression_3')]
Cielago_North_3_Troop_Markers = [(430, 530,'Cielago_North_3')]
Cielago_East_4_Troop_Markers = [(565, 665,'Cielago_East_4')]
South_Mesa_4_Troop_Markers = [(605,620,'South_Mesa_4')]
False_Wall_South_4_Troop_Markers = [(530, 565, 'False_Wall_South_4')]
Harg_Pass_4_Troop_Markers = [(440, 465, 'Harg_Pass_4')]
South_Mesa_5_Troop_Markers = [(640,590, 'South_Mesa_5')]
Tueks_Sietch_5_Troop_Markers = [(620, 545, 'Tueks_Sietch_5')]
False_Wall_South_5_Troop_Markers = [(555,505, 'False_Wall_South_5')]
Pasty_Mesa_5_Troop_Markers = [(580, 470, 'Pasty_Mesa_5')]
The_Minor_Erg_5_Troop_Markers = [(510, 465, 'The_Minor_Erg_5')]
Harg_Pass_5_Troop_Markers = [(465, 440, 'Harg_Pass_5')]
False_Wall_East_5_Troop_Markers = [(435, 410, 'False_Wall_East_5')]
False_Wall_East_6_Troop_Markers = [(435, 390, 'False_Wall_East_6')]
The_Minor_Erg_6_Troop_Markers = [(500, 405, 'The_Minor_Erg_6')]
Pasty_Mesa_6_Troop_Markers = [(615, 410, 'Pasty_Mesa_6')]
South_Mesa_6_Troop_Markers = [(695, 410, 'South_Mesa_6')]
False_Wall_East_7_Troop_Markers = [(435, 370, 'False_Wall_East_7')]
The_Minor_Erg_7_Troop_Markers = [(520, 355, 'The_Minor_Erg_7')]
Pasty_Mesa_7_Troop_Markers = [(615, 365, 'Pasty_Mesa_7')]
Red_Chasm_7_Troop_Markers = [(695, 335, 'Red_Chasm_7')]
False_Wall_East_8_Troop_Markers = [(435, 350, 'False_Wall_East_8')]
The_Minor_Erg_8_Troop_Markers = [(515, 315, 'The_Minor_Erg_8')]
Pasty_Mesa_8_Troop_Markers = [(600, 275, 'Pasty_Mesa_8')]
Sheild_Wall_8_Troop_Markers = [(530, 285, 'Sheild_Wall_8')]
Gara_Kulon_8_Troop_Markers = [(630, 225, 'Gara_Kulon_8')]
False_Wall_East_9_Troop_Markers = [(440, 330, 'False_Wall_East_9')]
Sheild_Wall_9_Troop_Markers = [(510, 250, 'Sheild_Wall_9')]
Imperial_Basin_9_Troop_Markers = [(455, 295, 'Imperial_Basin_9')]
Hole_in_the_Rock_9_Troop_Markers = [(510, 220, 'Hole_in_the_Rock_9')]
Rim_Wall_West_9_Troop_Markers = [(530, 170, 'Rim_Wall_West_9')]
Basin_9_Troop_Markers = [(565, 140, 'Basin_9')]
OH_Gap_9_Troop_Markers = [(535, 100, 'OH_Gap_9')]
Sihaya_Ridge_9_Troop_Markers = [(610, 165, 'Sihaya_Ridge_9')]
Imperial_Basin_10_Troop_Markers = [(430, 210, 'Imperial_Basin_10')]
OH_Gap_10_Troop_Markers = [(520, 75, 'OH_Gap_10')]
Arrakeen_10_Troop_Markers = [(470, 145, 'Arrakeen_10')]
Imperial_Basin_11_Troop_Markers = [(405, 250, 'Imperial_Basin_11')]
Arsunt_11_Troop_Markers = [(380, 290, 'Arsunt_11')]
Carthag_11_Troop_Markers = [(360, 175, 'Carthag_11')]
Tsimpo_11_Troop_Markers = [(355, 85, 'Tsimpo_11')]
OH_Gap_11_Troop_Markers = [(430, 45, 'OH_Gap_11')]
Broken_Land_11_Troop_Markers = [(350, 60, 'Broken_Land_11')]
Arsunt_12_Troop_Markers = [(370, 320, 'Arsunt_12')]
Hagga_Basin_12_Troop_Markers = [(315, 240, 'Hagga_Basin_12')]
Tsimpo_12_Troop_Markers = [(285, 150, 'Tsimpo_12')]
Broken_Land_12_Troop_Markers = [(235, 80, 'Broken_Land_12')]
Plastic_Basin_12_Troop_Markers = [(245, 115, 'Plastic_Basin_12')]
Hagga_Basin_13_Troop_Markers = [(255, 240, 'Hagga_Basin_13')]
Plastic_Basin_13_Troop_Markers = [(180, 185, 'Plastic_Basin_13')]
Tsimpo_13_Troop_Markers = [(250, 190, 'Tsimpo_13')]
Rock_Outcroppings_13_Troop_Markers = [(160, 130, 'Rock_Outcroppings_13')]
Wind_Pass_14_Troop_Markers = [(310, 345, 'Wind_Pass_14')]
Plastic_Basin_14_Troop_Markers = [(190, 275, 'Plastic_Basin_14')]
Bight_of_the_Cliff_14_Troop_Markers = [(125, 280, 'Bight_of_the_Cliff_14')]
Rock_Outcroppings_14_Troop_Markers = [(110, 180, 'Rock_Outcroppings_14')]
Sietch_Tabr_14_Troop_Markers = [(105, 255, 'Sietch_Tabr_14')]
Wind_Pass_15_Troop_Markers = [(310, 375, 'Wind_Pass_15')]
The_Great_Flat_15_Troop_Markers = [(195, 370, 'The_Great_Flat_15')]
Funeral_Plain_15_Troop_Markers = [(155, 335, 'Funeral_Plain_15')]
Bight_of_the_Cliff_15_Troop_Markers = [(60, 280, 'Bight_of_the_Cliff_15')]
Wind_Pass_16_Troop_Markers = [(285, 405, 'Wind_Pass_16')]
False_Wall_West_16_Troop_Markers = [(225, 425, 'False_Wall_West_16')]
The_Greater_Flat_16_Troop_Markers = [(80, 425, 'The_Greater_Flat_16')]
Habbanya_Erg_16_Troop_Markers = [(105, 475, 'Habbanya_Erg_16')]
Wind_Pass_North_17_Troop_Markers = [(310, 440, 'Wind_Pass_North_17')]
Wind_Pass_17_Troop_Markers = [(275, 465, 'Wind_Pass_17')]
False_Wall_West_17_Troop_Markers = [(210, 495, 'False_Wall_West_17')]
Habbanya_Erg_17_Troop_Markers = [(170, 470, 'Habbanya_Erg_17')]
Habbanya_Ridge_Flat_17_Troop_Markers = [(70, 520, 'Habbanya_Ridge_Flat_17')]
Habbanya_Ridge_Sietch_17_Troop_Markers = [(145, 520, 'Habbanya_Ridge_Sietch_17')]
Wind_Pass_North_18_Troop_Markers = [(295, 490, 'Wind_Pass_North_18')]
Cielago_West_18_Troop_Markers = [(255, 555, 'Cielago_West_18')]
False_Wall_West_18_Troop_Markers = [(220, 580, 'False_Wall_West_18')]
Habbanya_Ridge_Flat_18_Troop_Markers = [(170, 610, 'Habbanya_Ridge_Flat_18')]

def territories_troop_markers_get(territory):
    troop_markers = {
        'Arrakeen_10': Arrakeen_10_Troop_Markers,
        'Arsunt_11': Arsunt_11_Troop_Markers,
        'Arsunt_12': Arsunt_12_Troop_Markers,
        'Basin_9': Basin_9_Troop_Markers,
        'Bight_of_the_Cliff_14': Bight_of_the_Cliff_14_Troop_Markers,
        'Bight_of_the_Cliff_15': Bight_of_the_Cliff_15_Troop_Markers,
        'Broken_Land_11': Broken_Land_11_Troop_Markers,
        'Broken_Land_12': Broken_Land_12_Troop_Markers,
        'Cielago_Depression_1': Cielago_Depression_1_Troop_Markers,
        'Cielago_Depression_2': Cielago_Depression_2_Troop_Markers,
        'Cielago_Depression_3': Cielago_Depression_3_Troop_Markers,
        'Cielago_West_1': Cielago_West_1_Troop_Markers,
        'Cielago_West_18': Cielago_West_18_Troop_Markers,
        'Cielago_North_1': Cielago_North_1_Troop_Markers,
        'Cielago_North_2': Cielago_North_2_Troop_Markers,
        'Cielago_North_3': Cielago_North_3_Troop_Markers,
        'Cielago_South_2': Cielago_South_2_Troop_Markers,
        'Cielago_South_3': Cielago_South_3_Troop_Markers,
        'Cielago_East_3': Cielago_East_3_Troop_Markers,
        'Cielago_East_4': Cielago_East_4_Troop_Markers,
        'Carthag_11': Carthag_11_Troop_Markers,
        'False_Wall_East_5': False_Wall_East_5_Troop_Markers,
        'False_Wall_East_6': False_Wall_East_6_Troop_Markers,
        'False_Wall_East_7': False_Wall_East_7_Troop_Markers,
        'False_Wall_East_8': False_Wall_East_8_Troop_Markers,
        'False_Wall_East_9': False_Wall_East_9_Troop_Markers,
        'False_Wall_South_4': False_Wall_South_4_Troop_Markers,
        'False_Wall_South_5': False_Wall_South_5_Troop_Markers,
        'Funeral_Plain_15': Funeral_Plain_15_Troop_Markers,
        'False_Wall_West_16': False_Wall_West_16_Troop_Markers,
        'False_Wall_West_17': False_Wall_West_17_Troop_Markers,
        'False_Wall_West_18': False_Wall_West_18_Troop_Markers,
        'Gara_Kulon_8': Gara_Kulon_8_Troop_Markers,
        'Habbanya_Erg_16': Habbanya_Erg_16_Troop_Markers,
        'Habbanya_Erg_17': Habbanya_Erg_17_Troop_Markers,
        'Habbanya_Ridge_Flat_17': Habbanya_Ridge_Flat_17_Troop_Markers,
        'Habbanya_Ridge_Flat_18': Habbanya_Ridge_Flat_18_Troop_Markers,
        'Habbanya_Ridge_Sietch_17': Habbanya_Ridge_Sietch_17_Troop_Markers,
        'Hagga_Basin_12': Hagga_Basin_12_Troop_Markers,
        'Hagga_Basin_13': Hagga_Basin_13_Troop_Markers,
        'Harg_Pass_4': Harg_Pass_4_Troop_Markers,
        'Harg_Pass_5': Harg_Pass_5_Troop_Markers,
        'Hole_in_the_Rock_9': Hole_in_the_Rock_9_Troop_Markers,
        'Imperial_Basin_9': Imperial_Basin_9_Troop_Markers,
        'Imperial_Basin_10': Imperial_Basin_10_Troop_Markers,
        'Imperial_Basin_11': Imperial_Basin_11_Troop_Markers,
        'Meridian_1': Meridian_1_Troop_Markers,
        'Meridian_2': Meridian_2_Troop_Markers,
        'OH_Gap_9': OH_Gap_9_Troop_Markers,
        'OH_Gap_10': OH_Gap_10_Troop_Markers,
        'OH_Gap_11': OH_Gap_11_Troop_Markers,
        'Pasty_Mesa_5': Pasty_Mesa_5_Troop_Markers,
        'Pasty_Mesa_6': Pasty_Mesa_6_Troop_Markers,
        'Pasty_Mesa_7': Pasty_Mesa_7_Troop_Markers,
        'Pasty_Mesa_8': Pasty_Mesa_8_Troop_Markers,
        'Plastic_Basin_12': Plastic_Basin_12_Troop_Markers,
        'Plastic_Basin_13': Plastic_Basin_13_Troop_Markers,
        'Plastic_Basin_14': Plastic_Basin_14_Troop_Markers,
        'Polar_Sink_0': PolarSink_0_Troop_Markers,
        'Red_Chasm_7': Red_Chasm_7_Troop_Markers,
        'Rim_Wall_West_9': Rim_Wall_West_9_Troop_Markers,
        'Rock_Outcroppings_13': Rock_Outcroppings_13_Troop_Markers,
        'Rock_Outcroppings_14': Rock_Outcroppings_14_Troop_Markers,
        'South_Mesa_5': South_Mesa_5_Troop_Markers,
        'South_Mesa_6': South_Mesa_6_Troop_Markers,
        'South_Mesa_4': South_Mesa_4_Troop_Markers,
        'Sheild_Wall_8': Sheild_Wall_8_Troop_Markers,
        'Sheild_Wall_9': Sheild_Wall_9_Troop_Markers,
        'Sietch_Tabr_14': Sietch_Tabr_14_Troop_Markers,
        'Sihaya_Ridge_9': Sihaya_Ridge_9_Troop_Markers,
        'The_Great_Flat_15': The_Great_Flat_15_Troop_Markers,
        'The_Greater_Flat_16': The_Greater_Flat_16_Troop_Markers,
        'The_Minor_Erg_5': The_Minor_Erg_5_Troop_Markers,
        'The_Minor_Erg_6': The_Minor_Erg_6_Troop_Markers,
        'The_Minor_Erg_7': The_Minor_Erg_7_Troop_Markers,
        'The_Minor_Erg_8': The_Minor_Erg_8_Troop_Markers,
        'Tsimpo_11': Tsimpo_11_Troop_Markers,
        'Tsimpo_12': Tsimpo_12_Troop_Markers,
        'Tsimpo_13': Tsimpo_13_Troop_Markers,
        'Tueks_Sietch_5': Tueks_Sietch_5_Troop_Markers,
        'Wind_Pass_14': Wind_Pass_14_Troop_Markers,
        'Wind_Pass_15': Wind_Pass_15_Troop_Markers,
        'Wind_Pass_16': Wind_Pass_16_Troop_Markers,
        'Wind_Pass_17': Wind_Pass_17_Troop_Markers,
        'Wind_Pass_North_17': Wind_Pass_North_17_Troop_Markers,
        'Wind_Pass_North_18': Wind_Pass_North_18_Troop_Markers,
    }
    return troop_markers.get(territory, Default_Markers)

Row_Invalid_Markers = []
Row_0_Markers = [OH_Gap_10_Troop_Markers, Tsimpo_11_Troop_Markers, OH_Gap_11_Troop_Markers, Broken_Land_11_Troop_Markers,\
                 Broken_Land_12_Troop_Markers]
Row_1_Markers = [OH_Gap_9_Troop_Markers, Basin_9_Troop_Markers, Rim_Wall_West_9_Troop_Markers, Sihaya_Ridge_9_Troop_Markers,\
                 Arrakeen_10_Troop_Markers, Carthag_11_Troop_Markers,Tsimpo_12_Troop_Markers, Plastic_Basin_12_Troop_Markers,
                 Plastic_Basin_13_Troop_Markers, Tsimpo_13_Troop_Markers, Rock_Outcroppings_13_Troop_Markers, Rock_Outcroppings_14_Troop_Markers]
Row_2_Markers = [Pasty_Mesa_8_Troop_Markers, Sheild_Wall_8_Troop_Markers, Gara_Kulon_8_Troop_Markers, Sheild_Wall_9_Troop_Markers,\
                 Imperial_Basin_9_Troop_Markers, Hole_in_the_Rock_9_Troop_Markers, Imperial_Basin_10_Troop_Markers,\
                 Imperial_Basin_11_Troop_Markers, Arsunt_11_Troop_Markers, Hagga_Basin_12_Troop_Markers, Hagga_Basin_13_Troop_Markers,\
                 Plastic_Basin_14_Troop_Markers,Bight_of_the_Cliff_14_Troop_Markers, Sietch_Tabr_14_Troop_Markers, Bight_of_the_Cliff_15_Troop_Markers]
Row_3_Markers = [PolarSink_0_Troop_Markers, False_Wall_East_6_Troop_Markers, False_Wall_East_7_Troop_Markers,\
                 The_Minor_Erg_7_Troop_Markers, Pasty_Mesa_7_Troop_Markers, Red_Chasm_7_Troop_Markers, False_Wall_East_8_Troop_Markers,\
                 The_Minor_Erg_8_Troop_Markers, False_Wall_East_9_Troop_Markers, Arsunt_12_Troop_Markers, Wind_Pass_14_Troop_Markers,\
                 Wind_Pass_15_Troop_Markers, The_Great_Flat_15_Troop_Markers, Funeral_Plain_15_Troop_Markers]
Row_4_Markers = [Harg_Pass_4_Troop_Markers, Pasty_Mesa_5_Troop_Markers, The_Minor_Erg_5_Troop_Markers, Harg_Pass_5_Troop_Markers,\
                 False_Wall_East_5_Troop_Markers, The_Minor_Erg_6_Troop_Markers, Pasty_Mesa_6_Troop_Markers, South_Mesa_6_Troop_Markers, \
                 Wind_Pass_16_Troop_Markers, False_Wall_West_16_Troop_Markers, The_Greater_Flat_16_Troop_Markers, \
                 Habbanya_Erg_16_Troop_Markers, Wind_Pass_North_17_Troop_Markers, Wind_Pass_17_Troop_Markers, \
                 False_Wall_West_17_Troop_Markers, Habbanya_Erg_17_Troop_Markers, Wind_Pass_North_18_Troop_Markers]
Row_5_Markers = [Cielago_West_1_Troop_Markers, Cielago_North_1_Troop_Markers, Cielago_North_2_Troop_Markers, Cielago_North_3_Troop_Markers,\
                 False_Wall_South_4_Troop_Markers, South_Mesa_5_Troop_Markers, Tueks_Sietch_5_Troop_Markers, False_Wall_South_5_Troop_Markers,\
                 Habbanya_Ridge_Flat_17_Troop_Markers, Habbanya_Ridge_Sietch_17_Troop_Markers, Cielago_West_18_Troop_Markers,\
                 False_Wall_West_18_Troop_Markers]
Row_6_Markers = [Cielago_Depression_1_Troop_Markers, Cielago_Depression_2_Troop_Markers, Cielago_South_2_Troop_Markers,\
                 Cielago_East_3_Troop_Markers, Cielago_Depression_3_Troop_Markers, Cielago_East_4_Troop_Markers, \
                 South_Mesa_4_Troop_Markers, Habbanya_Ridge_Flat_18_Troop_Markers]
Row_7_Markers = [Meridian_1_Troop_Markers, Meridian_2_Troop_Markers, Cielago_South_3_Troop_Markers]

def troop_markers_by_row(row_number):
    row_markers = {
        0: Row_0_Markers,
        1: Row_1_Markers,
        2: Row_2_Markers,
        3: Row_3_Markers,
        4: Row_4_Markers,
        5: Row_5_Markers,
        6: Row_6_Markers,
        7: Row_7_Markers,
    }
    return row_markers.get(row_number, Row_Invalid_Markers)
