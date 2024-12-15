import fontTools
import fontTools.ttLib


def print_kerning_pairs(_font_path):
    font = fontTools.ttLib.TTFont(_font_path)

    if 'GPOS' not in font:
        print("Font don't have GPOS")
        return

    gpos = font['GPOS'].table

    for lookup in gpos.LookupList.Lookup:
        for subtable in lookup.SubTable:
            # Type 2 - pair kerning
            if subtable.LookupType == 2:
                if subtable.Format == 1:
                    for i, pairset in enumerate(subtable.PairSet):
                        first_glyph = subtable.Coverage.glyphs[i]
                        for pairvalue in pairset.PairValueRecord:
                            second_glyph = pairvalue.SecondGlyph
                            x_advance = pairvalue.Value1.XAdvance if pairvalue.Value1 else 0
                            print(f"Type 1. Pair: {first_glyph}, {second_glyph}, Value: {x_advance}")
                elif subtable.Format == 2:
                    print('Type 2')
                    # class1_records = subtable.Class1Record
                    # for class1_index, class1 in enumerate(class1_records):
                    #     for class2_index, class2 in enumerate(class1.Class2Record):
                    #         if class2.Value1:
                    #             x_advance = class2.Value1.XAdvance
                    #             if x_advance != 0:
                    #                 first_glyphs = [g for g, c in subtable.ClassDef1.classDefs.items() if
                    #                                 c == class1_index]
                    #                 second_glyphs = [g for g, c in subtable.ClassDef2.classDefs.items() if
                    #                                  c == class2_index]
                    #                 for first_glyph in first_glyphs:
                    #                     for second_glyph in second_glyphs:
                    #                          print(f"Type 2. Pair: {first_glyph}, {second_glyph}, "
                    #                                f"Value: {x_advance}")


font_path = "test_font.ttf"
print_kerning_pairs(font_path)
