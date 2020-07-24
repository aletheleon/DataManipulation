import copy


class Farm:
    company_name = "Orgo"

    def __init__(self, name, owner, country, size, num_of_livestock, num_of_workers, assets, compatible_livestock):
        self.name = name
        self.owner = owner
        self.country = country
        self.size = size
        self.num_of_livestock = num_of_livestock
        self.num_of_workers = num_of_workers
        self.assets = assets
        self.compatible_livestock = compatible_livestock

    def __lt__(self, other):
        return self.assets < other.assets

    def __eq__(self, other):
        return self.name == other.name and self.owner == other.owner

    def __repr__(self):
        return f"{self.name}"


class Livestock:
    def __init__(self, name, price_in, utilizations):
        self.name = name
        self.price_in = price_in
        self.utilizations = utilizations

    def __lt__(self, other):
        return len(self.utilizations) < len(other.utilizations)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"{self.name}, {self.price_in}"


def clean_farm_data(raw_farm_data):
    for farm in raw_farm_data:
        farm[2] = farm[2].split()[-1]
        farm[3] = int(farm[3])
        farm[4] = int(farm[4])
        farm[5] = int(farm[5])
        farm[6] = int(farm[6])
        if farm[7] == {}:
            farm[7] = None
        else:
            livestock_str = ""
            for livestock in sorted(farm[7]):
                livestock_str += str(livestock).lower() + ";"
            farm[7] = livestock_str[:-1]
    return raw_farm_data


def clean_livestock_data(raw_livestock_data):
    for livestock in raw_livestock_data:
        livestock[0] = str(livestock[0]).lower()
        livestock[1] = float(livestock[1])
        if livestock[2]:  # Checks if has utilizations
            utilizations_str = ""
            for utilization in sorted(livestock[2].split(",")):
                if not utilization[-1].isalpha():
                    # Removes unnecessary punctuation
                    utilization = utilization[:-1]
                utilizations_str += str(utilization).lower() + ";"
            livestock[2] = utilizations_str[:-1]
        else:
            livestock[2] = None
    return raw_livestock_data


def create_farm_instances(farm_data):
    return [Farm(farm[0], farm[1], farm[2], farm[3], farm[4], farm[5], farm[6], farm[7]) for farm in farm_data]


def create_livestock_instances(livestock_data):
    return [Livestock(livestock[0], livestock[1], livestock[2]) for livestock in livestock_data]


def buy_new_livestock(livestock_list, livestock_quant, farm):
    num_bought = 0
    for k in range(len(livestock_list)):
        if str(livestock_list[k].name).lower() in farm.compatible_livestock.split(";"):
            farm.assets -= livestock_list[k].price_in * livestock_quant[k]
            num_bought += livestock_quant[k]
    farm.num_of_livestock += num_bought
    return num_bought


def mutate_workers(farm, num_changed, addition):
    farm.num_of_workers += num_changed if addition else -1 * num_changed


def sort_farms_assets(farms_list):
    return sorted(farms_list, key=lambda f: -f.assets)


def sort_farms_num_of_liv(farms_list):
    return sorted(farms_list, key=lambda f: -f.num_of_livestock)


def count_meat(livestock_list):
    return len([livestock for livestock in livestock_list if livestock.utilizations is not None and 'meat' in
                livestock.utilizations.split(';')])


def livestock_to_occurences(livestock_list_dup):
    liv_dict = {}
    for livestock in livestock_list_dup:
        if livestock.name in liv_dict.keys():
            liv_dict[livestock.name] += 1
        else:
            liv_dict[livestock.name] = 1
    return liv_dict


def remove_dup(livestock_list_dup):
    unique_liv = []
    for livestock in livestock_list_dup:
        if livestock not in unique_liv:
            unique_liv.append(livestock)
    return unique_liv


def livestock_objs_to_dict(livestock_list):
    return {livestock.name: (livestock.price_in, livestock.utilizations) for livestock in livestock_list}


def farm_to_density(farms_list):
    return {farm.name: farm.num_of_livestock / farm.size for farm in farms_list}


def livestock_to_util(livestock_list):
    return {livestock.name: len(str(livestock.utilizations).split(';')) if livestock.utilizations else 0 for livestock
            in livestock_list}


def shortage_or_surplus(demand_list, supply_list):
    return [supply - demand for demand, supply in zip(demand_list, supply_list)]


def livestock_to_shortage(livestock_list, diff):
    return {livestock.name: diff_element for livestock, diff_element in zip(livestock_list, diff) if diff_element < 0}


def livestock_shallow_copy(livestock_list):
    return copy.copy(livestock_list)


def livestock_deep_copy(livestock_list):
    return copy.deepcopy(livestock_list)


def main():
    raw_farm_data = [
                    # name, owner, country, size, number of livestock, number of workers, assets, compatible livestock
                    ['2316 TA Family Farm', 'Melinda McDaniel', 'Atlanta, GA, USA', '1600', '3000', '7', '6000000', {'Dog', 'Goat', 'Pig', 'Python', 'Cattle', 'Donkey'}],
                    ['Schrute Beets Farm', 'Dwight Schrute', 'Scranton, PA, USA', '300', '860', '4', '55000', {'Pig', 'Llama', 'Cattle', 'Dog', 'Deer'}],
                    ['Dairy Farm of Lady Mary', 'Mary Crawley', 'Hampshire, UK', '2000', '749', '30', '1100000', {'Goat', 'Donkey', 'Cattle', 'Sheep', 'Horse'}],
                    ["Gollum's Furry Things Farm", 'Gollum', 'Brisbane, Queensland, Australia', '550', '90', '23', '150000', {'Goat', 'Sheep', 'Dog', 'Llama', 'Rabbit', 'Camel'}],
                    ['Santa Claus Independent Farm', 'Santa Claus', 'Lapland, Finland', '760', '60', '1', '14400', {'Reindeer', 'Llama'}],
                    ['Scott Family Farm', 'Michael Scott', 'Canada', '300', '50', '10', '230000', {'Horse', 'Mule', 'Donkey', 'Pig'}],
                    ['Organic Veggie Farm', 'Jim Halpert', 'New Mexico, USA', '230', '0', '20', '88000', {}]
                    ]

    raw_livestock_data = [
                # name, price_in, utilizations
                ['Dog', '200.0', 'Draught,Hunting,Herding,Searching,Guarding.'],
                ['Goat', '1000.0', 'Dairy,Meat,Wool,Leather.'],
                ['Python', '10000.3', ''],
                ['Cattle', '2000.75', 'Meat,Dairy,Leather,Draught.'],
                ['Donkey', '3400.01', 'Draught,Meat,Dairy.'],
                ['Pig', '900.5', 'Meat,Leather.'],
                ['Llama', '5000.66', 'Draught,Meat,Wool.'],
                ['Deer', '920.32', 'Meat,Leather.'],
                ['Sheep', '1300.12', 'Wool,Dairy,Leather,Meat.'],
                ['Rabbit', '100.0', 'Meat,Fur.'],
                ['Camel', '1800.9', 'Meat,Dairy,Mount.'],
                ['Reindeer', '4000.55', 'Meat,Leather,Dairy,Draught.'],
                ['Mule', '4400.2', 'Draught.'],
                    ]

    live_dict_dup = [
                ['Dog', '200.0', 'Draught,Hunting,Herding,Searching,Guarding.'],
                ['Goat', '1000.0', 'Dairy,Meat,Wool,Leather.'],
                ['Python', '10000.3', ''],
                ['Cattle', '2000.75', 'Meat,Dairy,Leather,Draught.'],
                ['Dog', '200.0', 'Draught,Hunting,Herding,Searching,Guarding.'],
                ['Goat', '1000.0', 'Dairy,Meat,Wool,Leather.'],
                ['Python', '10000.3', ''],
                ['Dog', '2000.75', 'Meat,Dairy,Leather,Draught.']
            ]

    print(livestock_to_occurences(create_livestock_instances(clean_livestock_data(live_dict_dup))))
    print(livestock_objs_to_dict(create_livestock_instances(clean_livestock_data(live_dict_dup))))


if __name__ == '__main__':
    main()
