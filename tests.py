from balancer import app


def test_index_returns_200():
    request, response = app.test_client.get('/')
    assert response.status == 200


def test_urls_count():
    params = {'video': 'http://s1.origin-cluster/video/1488/xcg2djHckad.m3u8'}
    request_count = app.config.CDN_A_WEIGHT + app.config.CDN_B_WEIGHT + app.config.ORIGIN_WEIGHT
    cdn_a_urls = 0
    cdn_b_urls = 0
    origin_urls = 0
    client = app.test_client
    urls = []
    for i in range(request_count):
        request, responce = client.get('/', params=params)

        if app.config.CDN_A_HOST in responce.text:
            cdn_a_urls += 1
        elif app.config.CDN_B_HOST in responce.text:
            cdn_b_urls += 1
        else:
            origin_urls += 1
        urls.append(responce.text)

    print(urls)
    assert cdn_a_urls == app.config.CDN_A_WEIGHT
    assert cdn_b_urls == app.config.CDN_B_WEIGHT
    assert origin_urls == app.config.ORIGIN_WEIGHT
