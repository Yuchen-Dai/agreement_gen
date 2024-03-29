

class Product:
    def __init__(self, name: str , model: str, current: str, unit: str, raw_price: float, adjunct: list):
        assert type(name) == str
        self.name = name.strip("\n\t ")
        assert type(model) == str
        self.model = model.strip("\n\t ")
        assert type(current) == str
        self.current = current.strip("\n\t ")
        assert type(unit) == str
        self.unit = unit.strip("\n\t ")
        assert type(raw_price) in [int, float], f'price should be int or float, but recieve a {type(raw_price)}'
        self.raw_price = raw_price
        assert type(adjunct) == list, f'adjunct should be a list of tuple: [(adjunct_name, price)], but receive {type(adjunct)}'
        assert all(type(i) == tuple and len(i) == 2 for i in adjunct)
        assert all([type(i[0]) == str and (type(i[1]) == float or type(i[1]) == int) for i in adjunct])
        self.adjunct = [(i[0].strip("\n\t "), i[1]) for i in adjunct]  # [(adjunct_name, price)]

    def get_specs(self):
        result = self.model
        if self.current:
            result += f" {self.current}"
        if len(self.adjunct):
            result += ' ' + ' '.join([i[0] for i in self.adjunct])
        return result

    def get_model(self):
        result = self.model
        if self.current:
            result += f' {self.current}'
        return result

    def get_adjunct(self):
        return ' '.join([i[0] for i in self.adjunct])

    def get_name(self):
        return self.name

    def get_unit(self):
        return self.unit

    def get_raw_price(self):
        return self.raw_price

    def get_adjunct_price(self):
        return float(sum([i[1] for i in self.adjunct]))

    def copy(self):
        new_adjunct = [(i[0], i[1]) for i in self.adjunct]
        return Product(self.name, self.model, self.current, self.unit, self.raw_price, new_adjunct)

    def __lt__(self, other):
        if self.model < other.model:
            return True
        if self.model == other.model and self.current < other.current:
            return True
        if self.model == other.model and self.current == other.current and \
                len(self.get_adjunct()) < len(other.get_adjunct()):
            return True
        return False

    def __eq__(self, other):
        if self.model != other.model or self.current != other.current:
            return False
        if len(self.adjunct) != len(other.adjunct):
            return False
        name_list = [i[0] for i in other.adjunct]
        for i in self.adjunct:
            if i[0] not in name_list:
                return False
        return True

    def __repr__(self):
        return f'Product(name = {self.name}, model = {self.model}, current = {self.current}, unit = {self.unit}, ' \
               f'raw_price = {self.raw_price}, adjunct = {self.adjunct})'


if __name__ == '__main__':
    a = Product('塑壳断路器', 'RMM1-630S/3310', '500A', '台', 1220.00, [("抽屉式", 180), ("VC3", 30.1)])
    print(a)
    print(a.copy())
    print(a.get_adjunct_price())
    print(a.get_model())