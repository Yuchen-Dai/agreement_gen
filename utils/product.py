

class Product:
    def __init__(self, name:str , specs : list, unit: str, raw_price: float, adjunct_price:float):
        self.name = name
        self.specs = specs
        self.unit = unit
        self.raw_price = raw_price
        self.adjunct_price = adjunct_price

    def get_specs(self):
        return ' '.join(self.specs.values())

    def get_name(self):
        return self.name

    def get_unit(self):
        return self.unit

    def get_raw_price(self):
        return self.raw_price

    def get_adjunct_price(self):
        return self.adjunct_price

    def update_raw_price(self,p):
        self.raw_price = p

    def update_adjunct_price(self,p):
        self.adjunct_price = p

    def __repr__(self):
        return f'Product(name = {self.name}, specs = {self.specs}, unit = {self.unit}, ' \
               f'raw_price = {self.raw_price}, adjunct_price = {self.adjunct_price})'


if __name__ == '__main__':
    a = Product('塑壳断路器',{'RMM1-630S/3310', '500A'},'台','1220','130')
    print(a)
