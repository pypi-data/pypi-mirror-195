import requests

class request:
    def __init__(self, request):
        self.request = request
    
    def credentials (self):
        return self.request 
    

r = request('test')
print(r.credentials())