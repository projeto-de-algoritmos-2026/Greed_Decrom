
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

def _thousandfy(s):
    newsymbol = {}
    newsymbol['valor'] = s['valor'] * 1000
    reps = []
    for r in s['reps']:
        reps.append("\033[53m" + r + '\033[55m')
    newsymbol['reps'] = tuple(reps)
    return newsymbol

def _hunthousandfy(s):
    newsymbol = {}
    newsymbol['valor'] = s['valor'] * 100_000
    reps = []
    for r in s['reps']:
        reps.append("|\033[53m" + r + '\033[55m|')
    newsymbol['reps'] = tuple(reps)
    return newsymbol

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

    one = [{"valor": 1, "reps":("I", "i", "Ⅰ", "ⅰ")}]

    tens = [
        {"valor": 10, "reps":("X", "x", "Ⅹ", "ⅹ")},
        {"valor": 100, "reps":("C", "c", "Ⅽ", "ⅽ")}
    ]

    fives = [
        {"valor": 5, "reps":("V", "v", "Ⅴ", "ⅴ")},
        {"valor": 50, "reps":("L", "l", "Ⅼ", "ⅼ")}
    ] if not additive_long else []

    if not apostrophus:
        fives += [{"valor": 500, "reps":("D", "d", "Ⅾ", "ⅾ")}] if not additive_long else []
        if not vinculum:
            tens += [{"valor": 1000, "reps":("M", "m", "Ⅿ", "ⅿ")}]


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


    #subtractions

    subs = []

    if not additive_long:
        # subtract one from tens
        if not additive_nine:
            for t in tens:
                subs += _subtractUpTo(one[0], t, 1 if not subtractive_long else 3)
                if not subtractive_forms: break
        
        # subtract one from fives
        for f in fives:
            if f['valor'] == one[0]['valor'] * 5:
                if(additive_four): continue
                subs += _subtract(one[0], f, 1)    
                continue
            if additive_nine or not subtractive_forms: break
            subs += _subtract(one[0], f, 1)
        
        # subtract tens from tens
        if not additive_nines:
            for t1 in range(len(tens)-1):
                for t2 in range(t1+1, len(tens)):
                    subs += _subtractUpTo(tens[t1], tens[t2], 1 if not subtractive_long else 3)
                    if not subtractive_forms: break
        
        # subtract tens from fives
        for t in tens:
            for f in fives:
                if f['valor'] == t['valor'] * 5:
                    if additive_fours: continue
                    subs += _subtract(t, f, 1)
                    continue
                if f['valor'] < t['valor']: continue
                if additive_nines or not subtractive_forms: break
                subs += _subtract(t, f, 1)

        if subtractive_fives:
            # subtract fives from fives
            for f1 in range(len(fives)-1):
                for f2 in range(f1+1, len(fives)):
                    subs += _subtract(fives[f1], fives[f2], 1)
            
            # subtract fives from tens
            for f in fives:
                for t in tens:
                    if t['valor'] <= f['valor'] * 2: continue
                    subs += _subtract(f, t, 1)



    symbols += one + tens + fives

    if vinculum:
        tone =      [_thousandfy(one[0])]
        ttens =     [_thousandfy(t) for t in tens]
        del(ttens[-1])
        tfives =    [_thousandfy(f) for f in fives]
        if not additive_long: del(tfives[-1])
        tsymbols =  tone + ttens + tfives
        tsubs =     [_thousandfy(s) for s in subs if s['valor'] <= 50]


        vsubs = []

        # subtract one from thousands
        if subtractive_forms and not additive_nine:
            for th in tsymbols:
                vsubs += _subtractUpTo(one[0], th, 1 if not subtractive_long else 3)
            for ts in tsubs:
                vsubs += _subtractUpTo(one[0], ts, 1 if not subtractive_long else 3)

        # subtract tens from thousands
        if not additive_nines:
            for t in tens:
                for th in tsymbols:
                    if th['valor'] == t['valor'] * 10:
                        vsubs += _subtractUpTo(t, th, 1 if not subtractive_long else 3)
                        continue
                    if not subtractive_forms: break
                    vsubs += _subtractUpTo(t, th, 1 if not subtractive_long else 3)
            if subtractive_forms:
                for t in tens:
                    for ts in tsubs:
                        vsubs += _subtractUpTo(t, ts, 1 if not subtractive_long else 3)
        
        # subtract fives from thousands
        if subtractive_fives:
            for f in fives:
                for th in tsymbols:
                    if th['valor'] == f['valor'] * 2: continue
                    vsubs += _subtract(f, th, 1)
            for f in fives:
                for ts in tsubs:
                    vsubs += _subtract(f, ts, 1)

        if vinculum_large:
            htsymbols = [_hunthousandfy(s) for s in symbols]
            htsubs =    [_hunthousandfy(s) for s in subs]

            if subtractive_forms:
                # subtract one from hunthousands
                if not additive_nine:
                    for th in htsymbols:
                        vsubs += _subtractUpTo(one[0], th, 1 if not subtractive_long else 3)
                    for ts in htsubs:
                        vsubs += _subtractUpTo(one[0], ts, 1 if not subtractive_long else 3)

                # subtract tens from hunthousands
                if not additive_nines:
                    for t in tens:
                        for th in htsymbols:
                            vsubs += _subtractUpTo(t, th, 1 if not subtractive_long else 3)
                    for t in tens:
                        for ts in htsubs:
                            vsubs += _subtractUpTo(t, ts, 1 if not subtractive_long else 3)
                
                # subtract fives from hunthousands
                if subtractive_fives:
                    for f in fives:
                        for th in htsymbols:
                            vsubs += _subtract(f, th, 1)
                    for f in fives:
                        for ts in htsubs:
                            vsubs += _subtract(f, ts, 1)
            
        
            # subtract one thousand from hunthousands
            if not additive_nines:
                if subtractive_forms:
                    for th in htsymbols:
                        vsubs += _subtractUpTo(tone[0], th, 1 if not subtractive_long else 3)
                    for ts in htsubs:
                        vsubs += _subtractUpTo(tone[0], ts, 1 if not subtractive_long else 3)

            # subtract ten thounsands from hunthousands
            if not additive_nines:
                for t in ttens:
                    for th in htsymbols:
                        if th['valor'] == t['valor'] * 10:
                            vsubs += _subtractUpTo(t, th, 1 if not subtractive_long else 3)
                            continue
                        if not subtractive_forms: break
                        vsubs += _subtractUpTo(t, th, 1 if not subtractive_long else 3)
                if subtractive_forms:
                    for t in ttens:
                        for ts in htsubs:
                            vsubs += _subtractUpTo(t, ts, 1 if not subtractive_long else 3)
            
            # subtract fives thousands from hunthousands
            if subtractive_fives:
                for f in tfives:
                    for th in htsymbols:
                        if th['valor'] == f['valor'] * 2: continue
                        vsubs += _subtract(f, th, 1)
                for f in tfives:
                    for ts in htsubs:
                        vsubs += _subtract(f, ts, 1)
            
            symbols += htsymbols + htsubs

        symbols += tsymbols + tsubs + vsubs

    symbols += subs
        

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