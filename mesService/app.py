# -*- coding: utf-8 -*-
# @createTime    : 2019/8/27 14:20
# @author  : Huanglg
# @fileName: manage.py
# @email: luguang.huang@mabotech.com
from mesService import create_app


app = create_app('development')

@app.after_request
def after_request(response):
    """
    Post request processing - add CORS, cache control headers
    """
    # Enable CORS requests for local development
    # The following will allow the local angular-cli development environment to
    # make requests to this server (otherwise, you will get 403s due to same-
    # origin poly)
    response.headers.add('Access-Control-Allow-Origin',
                         '*')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,Set-Cookie,Cookie,Cache-Control,Pragma,Expires')  # noqa
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE')

    # disable caching all requests
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response


if __name__ == '__main__':
    app.run(debug=True)
    print(app.url_map)
    app.run()
