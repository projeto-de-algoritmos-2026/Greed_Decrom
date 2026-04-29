
def _subtract(left, right, amount):
    value = right['valor'] - left['valor'] * amount
    reps = []

    for i in range(4):
        reps.append((left['reps'][i] * amount) + right['reps'][i])

    return [{'valor': value, 'reps': tuple(reps)}]

def _subtractUpTo(left, right, amount):
    res = []
    for i in range(amount):
        res += _subtract(left, right, i+1)
    return res

def generateSymbols( 
                apostrophus,
                apostrophus_special,
                vinculum,
                vinculum_large,
                additive_long,
                additive_four,
                additive_fours,
                additive_nine,
                additive_nines,
                subtractive_forms,
                subtractive_long,
                subtractive_fives,
                implied_fractions,
                limited_fractions,
                expanded_fractions):

    symbols = []
    tens = [
        {"valor": 1, "reps":("I", "i", "Ⅰ", "ⅰ")},
        {"valor": 10, "reps":("X", "x", "Ⅹ", "ⅹ")},
        {"valor": 100, "reps":("C", "c", "Ⅽ", "ⅽ")},
    ]

    fives = [
        {"valor": 5, "reps":("V", "v", "Ⅴ", "ⅴ")},
        {"valor": 50, "reps":("L", "l", "Ⅼ", "ⅼ")}
    ] if not additive_long else []

    subs = []

    if not (vinculum or apostrophus):
        tens += [{"valor": 1000, "reps":("M", "m", "Ⅿ", "ⅿ")}]
        fives += [{"valor": 500, "reps":("D", "d", "Ⅾ", "ⅾ")}] if not additive_long else []

    elif apostrophus:
        if not apostrophus_special:
            tens += [
                {"valor": 1000, "reps":("CIↃ", "ciↄ", "ⅠↃ", "ⅰↄ")},
                {"valor": 10000, "reps":("CCIↃↃ", "cciↄↄ", "ⅭⅭⅠↃↃ ", "ⅽⅽⅰↄↄ")},
                {"valor": 100000, "reps":("CCCIↃↃↃ", "ccciↄↄↄ", "ⅭⅭⅭⅠↃↃↃ ", "ⅽⅽⅽⅰↄↄↄ")}
            ]
            fives += [
                {"valor": 500, "reps":("*IↃ", "*iↄ", "*ⅠↃ", "*ⅰↄ")},
                {"valor": 5000, "reps":("*IↃↃ", "*iↄↄ", "*ⅠↃↃ", "*ⅰↄↄ")},
                {"valor": 50000, "reps":("*IↃↃↃ", "*iↄↄↄ", "*ⅠↃↃↃ", "*ⅰↄↄↄ")}
            ] if not additive_long else []
        else:
            tens += [
                {"valor": 1000, "reps":("ↀ", "ↀ", "ↀ", "ↀ")},
                {"valor": 10000, "reps":("ↂ", "ↂ", "ↂ", "ↂ")},
                {"valor": 100000, "reps":("ↈ", "ↈ", "ↈ", "ↈ")}
            ]
            fives += [
                {"valor": 500, "reps":("Ⅾ", "Ⅾ", "Ⅾ", "Ⅾ")},
                {"valor": 5000, "reps":("ↁ", "ↁ", "ↁ", "ↁ")},
                {"valor": 50000, "reps":("ↇ", "ↇ", "ↇ", "ↇ")}
            ] if not additive_long else []


    for t in range(len(tens)-1): # subtract tens from tens
        for t2 in range(t+1, len(tens)):
            if(t == 0 and t2 == 1 and additive_nine): continue
            if(t2-t == 1 and additive_nines): continue
            if(t2 - t >= 2 and not subtractive_forms): continue
            subs += _subtractUpTo(tens[t], tens[t2], 1 if not subtractive_long else 3)

    for t in range(len(tens)-1): # subtract tens from fives
        for f in range(t, len(fives)):
            if(t == 0 and f == 0 and additive_four): continue
            if(t == f and additive_fours): continue
            if(t != f and not subtractive_forms): continue
            subs += _subtractUpTo(tens[t], fives[f], 1 if (t==f or not subtractive_long) else 3)
    
    if(subtractive_fives):
        for f in range(len(fives)-1): # subtract fives from tens
            for t in range(f+2, len(tens)):
                if(t-f != 2 and not subtractive_forms): continue
                subs += _subtract(fives[f], tens[t], 1)
        for f in range(len(fives)-1): # subtract fives from fives
            for f2 in range(f+1, len(fives)):
                if(f2 - f != 1 and not subtractive_forms): continue
                subs += _subtract(fives[f], fives[f2], 1)


    symbols += tens + fives + subs

    vinc = []

    if vinculum:
        for s in symbols:
            newsymbol = {}
            newsymbol['valor'] = s['valor'] * 1000
            reps = []
            for r in s['reps']:
                reps.append("\033[53m" + r + '\033[55m')
            newsymbol['reps'] = tuple(reps)
            vinc.append(newsymbol)
        
        if vinculum_large:
            for s in symbols:
                newsymbol = {}
                newsymbol['valor'] = s['valor'] * 100_000
                reps = []
                for r in s['reps']:
                    reps.append("|\033[53m" + r + '\033[55m|')
                newsymbol['reps'] = tuple(reps)
                vinc.append(newsymbol) 

    symbols += vinc

    fracs = []

    if not implied_fractions:
        fracs = [
            {"valor": 1/12, "reps": ("·","·","·","·")},
            {"valor": 6/12, "reps": ("S","s","S","s")}
        ]
        if not expanded_fractions:
            fracs += [
                {"valor": 2/12, "reps": (":",":",":",":")},
                {"valor": 3/12, "reps": ("∴","∴","∴","∴")},
                {"valor": 4/12, "reps": ("∷","∷","∷","∷")},
                {"valor": 5/12, "reps": ("⁙","⁙","⁙","⁙")}
            ]

        if not limited_fractions:
            fracs += [
                {"valor": 1/24, "reps": ("Є","є","Є","є")},
                {"valor": 1/48, "reps": ("~Ↄ","~ↄ","~Ↄ","~ↄ")},
                {"valor": 1/72, "reps": ("𐆓","ƨ","𐆓","ƨ")},
                {"valor": 1/144, "reps": ("𐆔","𐆔","𐆔","𐆔")},
                {"valor": 1/288, "reps": ("℈","℈","℈","℈")},
                {"valor": 1/1728, "reps": ("》","𐆕","》","𐆕")}
            ]
    symbols += fracs

    symbols = sorted(symbols, key= lambda d:d['valor'])

    return tuple(reversed(symbols))

def getPleaseJupiter():
    return ({"valor": 4, "reps":("IIII", "iiii", "ⅠⅠⅠⅠ", "ⅰⅰⅰⅰ")})

def getClockFace():
    return (
        {"valor": 1, "reps": ("I", "i",       "Ⅰ", "ⅰ")},
        {"valor": 2, "reps": ("II", "ii",     "Ⅱ", "ⅱ")},
        {"valor": 3, "reps": ("III", "iii",   "Ⅲ", "ⅲ")},
        {"valor": 4, "reps": ("IV", "iv",     "Ⅳ", "ⅳ")},
        {"valor": 5, "reps": ("V", "v",       "Ⅴ", "ⅴ")},
        {"valor": 6, "reps": ("VI", "vi",     "Ⅵ", "ⅵ")},
        {"valor": 7, "reps": ("VII", "vii",   "Ⅶ", "ⅶ")},
        {"valor": 8, "reps": ("VIII", "viii", "Ⅷ", "ⅷ")},
        {"valor": 9, "reps": ("IX", "ix",     "Ⅸ", "ⅸ")},
        {"valor": 10, "reps": ("X", "x",       "Ⅹ", "ⅹ")},
        {"valor": 11, "reps": ("XI", "xi",     "Ⅺ", "ⅺ")},
        {"valor": 12, "reps": ("XII", "xii",   "Ⅻ", "ⅻ")},
    )
def sesuncia(prevchar, lowercase):
    ses= ('Є' if not lowercase else 'є' ) + '·'
    if prevchar == '·':
        return ses
    if prevchar == ':':
        return '·' + ses
    if prevchar == '∴':
        return ':' + ses
    if prevchar == '∷':
        return '∴' + ses
    if prevchar == '⁙':
        return '∷' + ses
    return prevchar + ('Є' if not lowercase else 'є' )