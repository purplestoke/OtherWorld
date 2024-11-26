import requests

class OWIPFS:
    def __init__(self, ip='xxx.xxx.xx.x', port='5001'):
        self.__client = f'http://{ip}:{port}/api/v0/'

    # ADDS FILE TO IPFS AND STORES METADATA
    # RETURNS CID OF FILE
    def addFile(self, fin):
        try:
            with open(fin, 'rb') as file:
                response = requests.post(self.__client + 'add', files={'file': file})
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error adding file: {e}")
            return None


    def retrieveFile(self, cid):
        try:
            response = requests.post(self.__client + f'cat?arg={cid}')
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Error retrieving file: {cid}\n{e}")
            return None



file = 'Example.txt'

ipfs = OWIPFS()
#add_result = ipfs.addFile(file)
#if add_result:
#    print(add_result['Hash'])
file = ipfs.retrieveFile(cid='hash')
print(file)