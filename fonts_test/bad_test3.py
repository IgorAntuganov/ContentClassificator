from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.G_P_O_S_ import table_G_P_O_S_


def get_glyph_name_map(font):
    cmap = font['cmap'].getBestCmap()
    return {chr(unicode): glyph_name for unicode, glyph_name in cmap.items()}


def get_glyph_name(font, input_value):
    cmap = font['cmap'].getBestCmap()

    # Если входное значение - целое число, считаем его кодом Unicode
    if isinstance(input_value, int):
        unicode_value = input_value
        char = chr(unicode_value)
    # Если это строка длиной 1, обрабатываем как символ
    elif isinstance(input_value, str) and len(input_value) == 1:
        char = input_value
        unicode_value = ord(char)
    # В остальных случаях используем входное значение как есть
    else:
        char = str(input_value)
        unicode_value = None

    # Попытка 1: Поиск по имени символа
    if char in font.getReverseGlyphMap():
        return font.getReverseGlyphMap()[char]

    # Попытка 2: Поиск по Unicode (если у нас есть корректное значение Unicode)
    if unicode_value is not None and unicode_value in cmap:
        return cmap[unicode_value]

    # Попытка 3: Проверка, существует ли глиф с таким именем
    if char in font.getGlyphSet():
        return char

    # Попытка 4: Использование входного значения как имени глифа
    return str(input_value)


class KerningManager:
    def __init__(self, path_to_font: str, path_to_save: str):
        self.path_to_save = path_to_save
        self.font = TTFont(path_to_font)
        if 'GPOS' not in self.font:
            self.font['GPOS'] = newTable('GPOS')
            self.font['GPOS'].table = table_G_P_O_S_()
        self.gpos = self.font['GPOS'].table

    @staticmethod
    def add_kerning_pair_to_font(font, first_char, second_char, value):
        gpos = font['GPOS'].table

        first_glyph = get_glyph_name(font, first_char)
        second_glyph = get_glyph_name(font, second_char)

        if first_glyph == first_char:
            print(f"Warning: Using character '{first_char}' as glyph name for first glyph")
        if second_glyph == second_char:
            print(f"Warning: Using character '{second_char}' as glyph name for second glyph")

        for lookup in gpos.LookupList.Lookup:
            if lookup.LookupType == 2:  # Pair Adjustment
                for subtable in lookup.SubTable:
                    if subtable.Format == 1:  # Specific pairs
                        if first_glyph not in subtable.Coverage.glyphs:
                            subtable.Coverage.glyphs.append(first_glyph)
                            subtable.PairSet.append(otTables.PairSet())
                            subtable.PairSetCount = len(subtable.PairSet)

                        first_glyph_index = subtable.Coverage.glyphs.index(first_glyph)
                        pair_set = subtable.PairSet[first_glyph_index]

                        # Check if PairValueRecord exists, if not, create it
                        if not hasattr(pair_set, 'PairValueRecord'):
                            pair_set.PairValueRecord = []

                        # Check if the pair already exists
                        for pair in pair_set.PairValueRecord:
                            if pair.SecondGlyph == second_glyph:
                                pair.Value1.XAdvance = value
                                return True

                        # If pair doesn't exist, create a new one
                        new_pair = otTables.PairValueRecord()
                        new_pair.SecondGlyph = second_glyph
                        new_pair.Value1 = otTables.ValueRecord()
                        new_pair.Value1.XAdvance = value

                        pair_set.PairValueRecord.append(new_pair)
                        pair_set.PairValueCount = len(pair_set.PairValueRecord)

                        return True

        # If we get here, we didn't find a suitable subtable. We should create one.
        new_subtable = otTables.PairPos()
        new_subtable.Format = 1
        new_subtable.Coverage = otTables.Coverage()
        new_subtable.Coverage.Format = 1
        new_subtable.Coverage.glyphs = [first_glyph]
        new_subtable.PairSet = [otTables.PairSet()]
        new_subtable.PairSetCount = 1
        new_subtable.ValueFormat1 = 4  # XAdvance
        new_subtable.ValueFormat2 = 0

        new_pair = otTables.PairValueRecord()
        new_pair.SecondGlyph = second_glyph
        new_pair.Value1 = otTables.ValueRecord()
        new_pair.Value1.XAdvance = value

        new_subtable.PairSet[0].PairValueRecord = [new_pair]
        new_subtable.PairSet[0].PairValueCount = 1

        # Add new subtable to the first Lookup of type 2
        for lookup in gpos.LookupList.Lookup:
            if lookup.LookupType == 2:
                lookup.SubTable.append(new_subtable)
                return True

        # If no Lookup of type 2 exists, create one
        new_lookup = otTables.Lookup()
        new_lookup.LookupType = 2
        new_lookup.LookupFlag = 0
        new_lookup.SubTable = [new_subtable]
        new_lookup.SubTableCount = 1
        gpos.LookupList.Lookup.append(new_lookup)
        gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)

        return True

    def add_kerning_pair(self, first_glyph, second_glyph, value):
        return self.add_kerning_pair_to_font(self.font, first_glyph, second_glyph, value)

    def save_font(self, _inspect=False):
        if _inspect:
            self.inspect_gpos(self.font)
        self.consolidate_font_kerning()
        self.sort_gpos_coverage()
        self.consolidate_kerning_lookups()
        self.font.save(self.path_to_save)

    def consolidate_font_kerning(self):
        gpos = self.font['GPOS'].table
        all_pairs = {}

        # Извлекаем все пары
        for lookup in gpos.LookupList.Lookup:
            for subtable in lookup.SubTable:
                if subtable.LookupType == 2 and subtable.Format == 1:
                    for i, pairset in enumerate(subtable.PairSet):
                        first_glyph = subtable.Coverage.glyphs[i]
                        for pairvalue in pairset.PairValueRecord:
                            second_glyph = pairvalue.SecondGlyph
                            value = pairvalue.Value1.XAdvance
                            all_pairs[(first_glyph, second_glyph)] = value

        # Create a new GPOS table
        new_gpos = otTables.GPOS()
        new_gpos.Version = 0x00010000  # This is version 1.0 in fixed-point format

        # Create a new Lookup
        new_lookup = otTables.Lookup()
        new_lookup.LookupType = 2  # Set LookupType to 2 for Pair Adjustment Positioning
        new_lookup.LookupFlag = 0  # Set LookupFlag to 0 for no special flags

        # Create a new PairPos subtable
        new_subtable = otTables.PairPos()
        new_subtable.Format = 1  # Set Format to 1 for specific pairs
        new_subtable.Coverage = otTables.Coverage()
        new_subtable.Coverage.Format = 1
        new_subtable.Coverage.glyphs = []
        new_subtable.PairSet = []
        new_subtable.ValueFormat1 = 4  # 4 corresponds to XAdvance
        new_subtable.ValueFormat2 = 0  # We're not adjusting the second glyph

        # Add the subtable to the lookup
        new_lookup.SubTable = [new_subtable]

        # Create a new LookupList and add our lookup to it
        new_gpos.LookupList = otTables.LookupList()
        new_gpos.LookupList.Lookup = [new_lookup]

        # Set FeatureList and ScriptList (even if empty)
        new_gpos.FeatureList = otTables.FeatureList()
        new_gpos.FeatureList.FeatureRecord = []
        new_gpos.ScriptList = otTables.ScriptList()
        new_gpos.ScriptList.ScriptRecord = []

        self.font['GPOS'].table = new_gpos

        # Add all pairs to the new table
        for (first_glyph, second_glyph), value in all_pairs.items():
            self.add_kerning_pair_to_font(self.font, first_glyph, second_glyph, value)

    def sort_gpos_coverage(self):
        glyph_order = self.font.getGlyphOrder()

        # Create a dictionary mapping glyph names to their index
        glyph_id_map = {name: i for i, name in enumerate(glyph_order)}

        gpos = self.font['GPOS'].table
        for lookup in gpos.LookupList.Lookup:
            if lookup.LookupType == 2:  # Pair Adjustment
                for subtable in lookup.SubTable:
                    if subtable.Format == 1:
                        # Sort Coverage glyphs
                        subtable.Coverage.glyphs.sort(key=lambda g: glyph_id_map[g])

                        # Reorder PairSet to match the new Coverage order
                        new_pair_set = [None] * len(subtable.Coverage.glyphs)
                        for i, glyph in enumerate(subtable.Coverage.glyphs):
                            old_index = subtable.Coverage.glyphs.index(glyph)
                            new_pair_set[i] = subtable.PairSet[old_index]
                        subtable.PairSet = new_pair_set

    def consolidate_kerning_lookups(self):
        gpos = self.font['GPOS'].table

        # Find all kerning lookups
        kerning_lookups = [l for l in gpos.LookupList.Lookup if l.LookupType == 2]

        if len(kerning_lookups) > 1:
            # Keep only the first kerning lookup
            main_kerning_lookup = kerning_lookups[0]

            # Remove other kerning lookups
            gpos.LookupList.Lookup = [l for l in gpos.LookupList.Lookup if l.LookupType != 2 or l == main_kerning_lookup]

            # Update FeatureList to reference only the main kerning lookup
            for feature in gpos.FeatureList.FeatureRecord:
                if feature.FeatureTag == 'kern':
                    feature.Feature.LookupListIndex = [gpos.LookupList.Lookup.index(main_kerning_lookup)]

        # Update LookupCount
        gpos.LookupList.LookupCount = len(gpos.LookupList.Lookup)

    @staticmethod
    def inspect_gpos(font):
        if 'GPOS' not in font:
            print("No GPOS table found in the font.")
            return

        gpos = font['GPOS'].table
        print(f"GPOS table version: {gpos.Version}")

        print("\nLookups:")
        for i, lookup in enumerate(gpos.LookupList.Lookup):
            print(f"  Lookup {i}:")
            print(f"    Type: {lookup.LookupType}")
            print(f"    Flag: {lookup.LookupFlag}")
            print(f"    SubTable count: {len(lookup.SubTable)}")

            for j, subtable in enumerate(lookup.SubTable):
                print(f"    SubTable {j}:")
                if hasattr(subtable, 'Format'):
                    print(f"      Format: {subtable.Format}")
                if hasattr(subtable, 'Coverage'):
                    print(f"      Coverage glyph count: {len(subtable.Coverage.glyphs)}")

        print("\nFeatures:")
        for i, feature in enumerate(gpos.FeatureList.FeatureRecord):
            print(f"  Feature {i}:")
            print(f"    Tag: {feature.FeatureTag}")
            print(f"    Lookup count: {len(feature.Feature.LookupListIndex)}")

        print("\nScripts:")
        for i, script in enumerate(gpos.ScriptList.ScriptRecord):
            print(f"  Script {i}:")
            print(f"    Tag: {script.ScriptTag}")
            for lang in script.Script.LangSysRecord:
                print(f"      Language: {lang.LangSysTag}")


if __name__ == '__main__':
    manager = KerningManager('test_font.ttf', 'extended.ttf')
    # manager.consolidate_font_kerning()
    manager.add_kerning_pair('P', 'P', 102)
    manager.save_font()
