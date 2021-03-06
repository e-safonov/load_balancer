CDN_A_HOST = '10.212.4.20'
CDN_B_HOST = '10.212.4.21'

CDN_A_WEIGHT = 1
CDN_B_WEIGHT = 2
ORIGIN_WEIGHT = 10

REDIS_URL = 'redis://redis_local:6379'
# REDIS_URL = 'redis://localhost:6379'
REDIS_CLEAN_START = False   # True not required for test_urls_count because server restarts per request in this test

HOST = '0.0.0.0'
PORT = '9999'
