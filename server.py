import web
from lib.mwmatching import maxWeightMatching

class Server:
    def POST(self):
        try:
            data = web.data()

            web.header('Content-Type', 'application/json')

            return '{ result: "Hello World" }'
        except:
            print('Exception while processing request!')


if __name__ == '__main__':
    urls = ('/', 'index')
    app = web.application(urls)
    app.run()
