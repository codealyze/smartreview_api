import os
from DB_mysql import DB
def all_stats():
    total = len(os.listdir('data/testimages'))
    db = DB('root', 'root', 'srlogs')
    result = db.query("select fraud from srlogs order by sno desc limit {}".format(total))
    from collections import Counter
    result = [eval(j) for i in result for j in i]
    counts = Counter(result)
    stats = {
        "checks_total": total,
        "checks_read": total,
        "errors":0,
        "clean_checks": counts[False],
        "fraud_checks": counts[True],
        "invalid":0,
    }
    return stats
