import os,sys,requests,json,time,random
# https://developers.rebrandly.com/reference/getlinks

class core(object):
    def __init__(self, apikey, workspace=None,log=False):
        self.headers = {
            "accept": "application/json",
            'apikey':apikey
        }
        if workspace:
            self.headers['workspace'] = workspace

        self.url="https://api.rebrandly.com/v1"
        self.__links = []
        self.account = requests.get(self.url + "/account", headers=self.headers).json()
        self.log = log

    def links(self,all=False,refresh=False):
        if self.__links == [] or refresh:
            self.__links = []

            baseurl = self.url + "/links?" + "&".join([
                "orderBy=createdAt",
                "orderDir=desc",
                "limit=25",
                "creator.id={0}".format(self.account['id']),
            ])
            url = str(baseurl)

            while True:
                response = requests.get(url, headers=self.headers)

                if response.status_code != 200:
                    print("Error Code {0}".format(response.status_code))
                    break

                self.__links += response.json()

                if not all:
                    break

                if len(response.json()) != 25:
                    break

                url = baseurl + "&last=" + self.__links[-1]['id']
                time.sleep(random.randint(1,5))

        return self.__links

    def get_link(self, link_id):
        response = requests.get(self.url + "/links/" + link_id, headers=self.headers)
        return response.json()

    def update_link(self,link_id, destination):
        response = requests.post(self.url + "/links/" + link_id, json={
            "destination": destination,
            #"title": "The Link for {0}".format(destination)
        },headers=self.headers)

        if self.log:
            print("Creating link {0} has the response code {1}".format(destination, response.status_code))

        if response.status_code != 200 and self.log:
            print("Error Text :> {0}".format(response.text))

        for link in self.links():
            if link['id'] == link_id:
                link['destination'] = destination
                #link['title'] = "The Link for {0}".format(destination)
                break

        return response.status_code == 200

    def create_link(self, destination, shortname):
        response = requests.get(url=self.url + "/links/new?" + "&".join([
            "destination={0}".format(destination),
            #"title=The Link for {0}".format(destination),
            "slashtag={0}".format(shortname)
        ]),headers=self.headers)

        if self.log:
            print("Creating link {0} has the response code {1}".format(shortname, response.status_code))

        if response.status_code == 200:
            self.__links.append(
                self.get_link(response.json()['id'])
            )
        elif self.log:
            print("Error Text :> {0}".format(response.text))
            

        return response.status_code == 200

    def create_or_update_link(self, destination, shortname):
        for link in self.links():
            if link['slashtag'] == shortname:
                if self.log:
                    print('Link Exists Already')
                return self.update_link(link['id'], destination)
        if self.log:
            print("Link Does not exist")
        return self.create_link(destination, shortname)