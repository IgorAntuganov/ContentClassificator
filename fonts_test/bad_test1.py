from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.G_P_O_S_ import table_G_P_O_S_


class KerningManager:
    def __init__(self, path_to_font: str, path_to_save: str):
        self.path_to_save = path_to_save
        self.font = TTFont(path_to_font)
        if 'GPOS' not in self.font:
            self.font['GPOS'] = newTable('GPOS')
            self.font['GPOS'].table = table_G_P_O_S_()
        self.gpos = self.font['GPOS'].table

    def add_kerning_pair(self, first_glyph, second_glyph, value):
        gpos = self.gpos
        return self.__add_kerning_pair(gpos, first_glyph, second_glyph, value)

    @staticmethod
    def __add_kerning_pair(gpos, first_glyph, second_glyph, value):
        for lookup in gpos.LookupList.Lookup:
            # print(lookup)
            # print(lookup.__dict__)
            if lookup.LookupType == 2:  # Pair Adjustment
                for subtable in lookup.SubTable:
                    if subtable.LookupType == 2 and subtable.Format == 1:
                        first_glyph_index = subtable.Coverage.glyphs.index(first_glyph)
                        pairset = subtable.PairSet[first_glyph_index]

                        new_pair = otTables.PairValueRecord()  # PyCharm highlighting is invalid
                        new_pair.SecondGlyph = second_glyph
                        new_pair.Value1 = otTables.ValueRecord()
                        new_pair.Value1.XAdvance = value

                        pairset.PairValueRecord.append(new_pair)
                        return True
                    return False

    def save_font(self):
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

        new_gpos = otTables.GPOS()

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

        # Add all pairs to the new table
        for (first_glyph, second_glyph), value in all_pairs.items():
            self.__add_kerning_pair(new_gpos, first_glyph, second_glyph, value)

        self.font['GPOS'].table = new_gpos


if __name__ == '__main__':
    manager = KerningManager('test_font.ttf', 'kerned_font.ttf')
    manager.consolidate_font_kerning()
    # manager.add_kerning_pair('T', 'T', 14)
    manager.save_font()
