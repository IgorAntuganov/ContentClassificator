import fontTools
import fontTools.ttLib


def print_kerning_pairs(_font_path):
    count = 0
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
                            count += 1
                elif subtable.Format == 2:
                    print('Type 2')
    print('Kerning pairs count:', count)


if __name__ == '__main__':
    font_path = "consolidated_gposOK_font.ttf"
    print_kerning_pairs(font_path)
