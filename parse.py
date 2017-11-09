import sys
from collections import defaultdict

filename = sys.argv[1]
with open(sys.argv[1]) as f:
    # 28/09/2017|PURCHASE WITH CARD 5402XXXXXXXX3033 AMAZON.ES COMPRA-amazon.es/ayu|01/10/2017|-10.49|867.78||5402051859783033

    categories = {
        'grocery': ("CAL FRUITOS", "CONDIS", "BON PREU", "DA GIORGIO", "SUPERVERD", "VERITAS", "ECOBOTIGA", "Macxipa",
                    "OLE MART", "CARMEN DECORACION", "ESTEL DE MAR"),
        'online': ("AMAZON", "FNAC"),
        "bills": ("TELEFONICA", "gas", "ELECTRICITY", "WATER", "FINQUES PARLA"),
        "ignore": ("WITHDRAWAL", "DIRECT DEBIT BSSG", "LOANS INSTALLMENT DEBIT")
    }

    transactions_by_category = defaultdict(list)

    for line in f.readlines():
        date1, concept, date2, amount_str, balance, _ = line.split("|", 5)
        concept = concept.replace("PURCHASE WITH CARD 5402XXXXXXXX3033", "").replace("-BARCELONA", "").strip()
        amount = float(amount_str)
        if amount < 0:
            category = ''
            for cat, keywords in categories.items():
                for k in keywords:
                    if k.lower() in concept.lower():
                        category = cat
                        break
                if category:
                    break

            if category:
                transactions_by_category[category].append((date1, concept, -amount))
            else:
                transactions_by_category["unknown"].append((date1, concept, -amount))

    total = 0
    for cat, transactions in transactions_by_category.items():
        print(cat)
        sum = 0
        for t in transactions:
            print("  %s %7.2f    %s" % (t[0], t[2], t[1]))
            sum += t[2]
        if cat not in ("unknown", "ignore"):
            total += sum
        print("  ***    SUM=%7.2f" % sum)
        print("")
    print("TOTOAL=      %7.2f" % total)





