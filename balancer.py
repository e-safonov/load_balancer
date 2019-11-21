from random import shuffle as random_shuffle

from sanic import Sanic
from sanic.response import text, redirect
from aioredis import create_redis_pool


app = Sanic()
app.config.from_pyfile('./config.py')


async def create_round_robin():
    rr = list()
    rr += [app.config.CDN_A_HOST] * app.config.CDN_A_WEIGHT
    rr += [app.config.CDN_B_HOST] * app.config.CDN_B_WEIGHT
    rr += ['origin'] * app.config.ORIGIN_WEIGHT
    random_shuffle(rr)
    return rr


async def get_url(video_url=None, origin_url=None):
    if not (video_url and origin_url):
        return text('error url not valid url format')

    host = await app.redis.rpoplpush('hosts', 'hosts', encoding='utf-8')
    if not host:
        return text('error host not found')
    elif host == 'origin':
        # return redirect(origin_url)
        return text(origin_url)
    else:
        # return redirect(f'http://{host}/{video_url}')
        return text(f'http://{host}/{video_url}')


async def parse_url(origin_url=''):
    video_url = ''
    if origin_url:
        parts = origin_url.split('/')
        if len(parts) > 3:
            video_url = '/'.join(parts[3:])
    return video_url, origin_url


@app.route('/', methods=['GET'])
async def main(request):
    video_url, origin_url = await parse_url(request.args.get('video'))
    res = await get_url(video_url, origin_url)
    return res


@app.listener('before_server_start')
async def init_redis(app, loop):
    app.redis = await create_redis_pool(app.config.REDIS_URL)
    llen = await app.redis.llen('hosts')
    if app.config.REDIS_CLEAN_START:
        await app.redis.ltrim('hosts', 0, 99)
        llen = 0

    if llen == 0:
        hosts_rr = await create_round_robin()
        await app.redis.rpush('hosts', *hosts_rr)


@app.listener('before_server_stop')
async def close_redis(app, loop):
    await app.redis.wait_closed()


if __name__ == '__main__':
    app.register_listener(init_redis, 'before_server_start')
    app.register_listener(close_redis, 'before_server_stop')
    app.run(host=app.config.HOST, port=app.config.PORT)
