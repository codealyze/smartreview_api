import os

stats = {
    "checks_total": len(os.listdir('data/testimages')),
    "checks_read": len(os.listdir('data/testimages')),
    "errors":0,
    "clean_checks": 3,
    "fraud_checks": 2,
    "invalid":0,
}
