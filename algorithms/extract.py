#! /usr/bin/env python

class Food(object):

    def __init__(self, fields):
        self.product_name                       = fields[7]
        self.quantity                           = fields[9]
        self.manufacturing_places               = fields[19]
        self.ingredients_text                   = fields[34]
        self.allergens                          = fields[35]
        self.traces                             = fields[37]
        self.traces_tags                        = fields[38]
        self.serving_size                       = fields[39]
        self.additives                          = fields[42]
        self.additives_tags                     = fields[43]
        self.ingredients_from_palm_oil          = fields[46]
        self.ingredients_from_palm_oil_tags     = fields[47]
        self.main_category                      = fields[58]
        self.image_url                          = fields[60]
        self.image_small_url                    = fields[61]
        self.energy_100g                        = fields[62]
        self.fat_100g                           = fields[63]
        self.saturated_fat_100g                 = fields[64]
        self.butyric_acid_100g                  = fields[65]
        self.caproic_acid_100g                  = fields[66]
        self.caprylic_acid_100g                 = fields[67]
        self.capric_acid_100g                   = fields[68]
        self.lauric_acid_100g                   = fields[69]
        self.myristic_acid_100g                 = fields[70]
        self.palmitic_acid_100g                 = fields[71]
        self.stearic_acid_100g                  = fields[72]
        self.arachidic_acid_100g                = fields[73]
        self.behenic_acid_100g                  = fields[74]
        self.lignoceric_acid_100g               = fields[75]
        self.cerotic_acid_100g                  = fields[76]
        self.montanic_acid_100g                 = fields[77]
        self.melissic_acid_100g                 = fields[78]
        self.monounsaturated_fat_100g           = fields[79]
        self.polyunsaturated_fat_100g           = fields[80]
        self.omega_3_fat_100g                   = fields[81]
        self.alpha_linolenic_acid_100g          = fields[82]
        self.eicosapentaenoic_acid_100g         = fields[83]
        self.docosahexaenoic_acid_100g          = fields[84]
        self.omega_6_fat_100g                   = fields[85]
        self.linoleic_acid_100g                 = fields[86]
        self.arachidonic_acid_100g              = fields[87]
        self.gamma_linolenic_acid_100g          = fields[88]
        self.dihomo_gamma_linolenic_acid_100g   = fields[89]
        self.omega_9_fat_100g                   = fields[90]
        self.oleic_acid_100g                    = fields[91]
        self.elaidic_acid_100g                  = fields[92]
        self.gondoic_acid_100g                  = fields[93]
        self.mead_acid_100g                     = fields[94]
        self.erucic_acid_100g                   = fields[95]
        self.nervonic_acid_100g                 = fields[96]
        self.trans_fat_100g                     = fields[97]
        self.cholesterol_100g                   = fields[98]
        self.carbohydrates_100g                 = fields[99]
        self.sugars_100g                        = fields[100]
        self.sucrose_100g                       = fields[101]
        self.glucose_100g                       = fields[102]
        self.fructose_100g                      = fields[103]
        self.lactose_100g                       = fields[104]
        self.maltose_100g                       = fields[105]
        self.maltodextrins_100g                 = fields[106]
        self.starch_100g                        = fields[107]
        self.polyols_100g                       = fields[108]
        self.fiber_100g                         = fields[109]
        self.proteins_100g                      = fields[110]
        self.casein_100g                        = fields[111]
        self.serum_proteins_100g                = fields[112]
        self.nucleotides_100g                   = fields[113]
        self.salt_100g                          = fields[114]
        self.sodium_100g                        = fields[115]
        self.alcohol_100g                       = fields[116]
        self.vitamin_a_100g                     = fields[117]
        self.vitamin_d_100g                     = fields[118]
        self.vitamin_e_100g                     = fields[119]
        self.vitamin_k_100g                     = fields[120]
        self.vitamin_c_100g                     = fields[121]
        self.vitamin_b1_100g                    = fields[122]
        self.vitamin_b2_100g                    = fields[123]
        self.vitamin_pp_100g                    = fields[124]
        self.vitamin_b6_100g                    = fields[125]
        self.vitamin_b9_100g                    = fields[126]
        self.vitamin_b12_100g                   = fields[127]
        self.biotin_100g                        = fields[128]
        self.pantothenic_acid_100g              = fields[129]
        self.silica_100g                        = fields[130]
        self.bicarbonate_100g                   = fields[131]
        self.potassium_100g                     = fields[132]
        self.chloride_100g                      = fields[133]
        self.calcium_100g                       = fields[134]
        self.phosphorus_100g                    = fields[135]
        self.iron_100g                          = fields[136]
        self.magnesium_100g                     = fields[137]
        self.zinc_100g                          = fields[138]
        self.copper_100g                        = fields[139]
        self.manganese_100g                     = fields[140]
        self.fluoride_100g                      = fields[141]
        self.selenium_100g                      = fields[142]
        self.chromium_100g                      = fields[143]
        self.molybdenum_100g                    = fields[144]
        self.iodine_100g                        = fields[145]
        self.caffeine_100g                      = fields[146]
        self.taurine_100g                       = fields[147]
        self.ph_100g                            = fields[148]
        self.fruits_vegetables_nuts_100g        = fields[149]
        self.collagen_meat_protein_ratio_100g   = fields[150]
        self.carbon_footprint_100g              = fields[151]

    def print(self):
        pass

def print_fields(fields):
    print(fields[7])
    print(fields[9])
    print(fields[17])
    print(fields[18])
    print(fields[19])
    print(fields[20])
    print(fields[34])
    print(fields[35])
    print(fields[37])
    print(fields[38])
    print(fields[39])
    print(fields[42])
    print(fields[43])
    print(fields[46])
    print(fields[47])
    print(fields[58])
    print(fields[60])
    print(fields[61])
    for i in range(62, 152):
        print(fields[i])

def quick_print(attribute, s):
    if attribute != '':
        print(s + ": " + attribute)

def main():
    csv = "fr.openfoodfacts.org.products.csv"
    separator = "\t"
    with open(csv, "r") as f:
        #fields = f.readline().split(separator)
        #print_fields(fields)
        food_array = []
        # remove field names
        fields = f.readline()
        for line in f:
            fields = line.rstrip("\n").split(separator)
            assert(len(fields) == 154)
            food_array.append(Food(fields))
        #for f in food_array:
            #quick_print(f.image_url, "image_url")

if __name__ == '__main__':
    main()
