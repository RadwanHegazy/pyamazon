import requests
from bs4 import BeautifulSoup
import json



class AmazonSerach:
    def __init__ (self, **args) :
        if not args['keyword'] or not args['CountryName'] :
            return "Please enter the parameters"
        zone = args['CountryName']
        url = f'https://www.amazon.{zone}/'
        url = f'{url}s?k={args["keyword"]}'
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
        
        try : 
            pages = args['pages']
        except KeyError :
            pages = 1
        try :
            self.data = []
            for i in range(pages):
                req = requests.get(url+f'&page={i}',headers={'User-Agent':user_agent},allow_redirects=True)
                soup = BeautifulSoup(req.text,'html.parser')
                images = soup.findAll('img',{'class':'s-image'})
                titles = soup.findAll('span',{'class':'a-size-base-plus a-color-base a-text-normal'})
                prices = soup.findAll('span',{'class':'a-price-whole'})
                stars = soup.findAll('span',{'class':'a-icon-alt'})
                country_price = soup.findAll('span',{'class':'a-price-symbol'})
                if len(titles) == len(stars) == len(images) == len(prices) == len(country_price) :
                    for i in range(len(images)) :
                        self.data.append({
                            'title':titles[i].text,
                            'price':str(prices[i].text).split('.')[0] + f" {country_price[i].text}", 
                            'image':images[i].get('src'),
                            'stars':stars[i].text,
                        })
                else :
                    get_mined = min(len(stars), len(images), len(titles), len(prices))
                    for i in range(int(get_mined)) :
                        self.data.append({
                            'title':titles[i].text,
                            'price':str(prices[i].text).split('.')[0] + f" {country_price[i].text}",
                            'image':images[i].get('src'),
                            'stars':stars[i].text,
                        })
                # return json.dumps(self.data,indent=5)
            # return self.data
        except Exception as error :
            return f"Can't open the {url}\n{error}"
    


    def get_data (self) :
        if self.data:
            return self.data
        else :
            return "There is no data"
    
    def export_to_json(self, output_name) :

        if not self.data:
            return "There is no data"

        data = [{
            'products':[]
        }]


        for item in self.data :
            data[0]['products'].append(item)


        json_str = json.dumps(data[0],indent=4,ensure_ascii=False).encode('utf-8')


        with open (f'{output_name}.json','w',encoding='utf-8') as output :
            output.write(json_str.decode())