import random
import itertools


class MenuMakanan:
    def __init__(self, nama, harga):
        self.nama = nama
        self.harga = harga


class JadwalHarian:
    def __init__(self, hari, listMenu):
        self.hari = hari
        self.listMenu = [listMenu]


# Menu Makanan
ListMenu = [
    MenuMakanan("Tempe Kecap", 3000),
    MenuMakanan("Usus", 3000),
    MenuMakanan("Nasi Pecel", 10000),
    MenuMakanan("Ayam Geprek", 10000),
    MenuMakanan("Cap Jay", 3000),
    MenuMakanan("Tahu Tek", 12000),
    MenuMakanan("Sate Ayam", 10000),
    MenuMakanan("Bebek Goreng", 12000),
    MenuMakanan("Tempe Pedas", 3000),
    MenuMakanan("Kerang", 3000),
    MenuMakanan("Telur Goreng", 2000),
    MenuMakanan("Kentang Goreng", 3000),
    MenuMakanan("Teri Kacang", 3000),
    MenuMakanan("Krengsengan Hati", 4000),
    MenuMakanan("Mie Goreng", 4000),
    MenuMakanan("Pempek", 10000),
]


def initialize_chromosome(num_days):
    chromosome = []
    for _ in range(num_days):
        daily_menu = random.sample(ListMenu, 3)
        chromosome.append(daily_menu)
    return chromosome


def hitung_fitness(gen):
    total_cost = 0
    penalti = 0

    for i in gen:
        for x in i:
            total_cost += x.harga

    if total_cost >= 500000:
        penalti += total_cost - 500000

    # Cek Makanan Sama Kurang dari 3 Hari
    for i in range(3, len(gen), 3):
        joinlist = list(itertools.chain(*gen[i - 3 : i]))
        listMakanan = set(joinlist)
        if len(listMakanan) != 9:
            penalti += 9 - len(listMakanan)

    print(f"total cost : {total_cost} pinalti {penalti}")

    return 1 / (total_cost + penalti)


# Fungsi crossover (persilangan) untuk menghasilkan anak
def crossover(parent1, parent2):
    crossover_point1 = random.randint(0, len(parent1) - 5)
    crossover_point2 = random.randint(crossover_point1 + 1, len(parent1) - 1)
    child = (
        parent1[:crossover_point1]
        + parent2[crossover_point1:crossover_point2]
        + parent1[crossover_point2:]
    )

    return child


def mutation(child):
    return random.shuffle(child)


def geneticAlgo(population, generation, mutation_probability):
    generate_population = [initialize_chromosome(30) for _ in range(population)]

    for _ in range(generation):
        new_population = []

        for _ in range(population):
            parent1 = random.choice(generate_population)
            parent2 = random.choice(generate_population)

            child = crossover(parent1, parent2)
            if random.random() < mutation_probability:  # Gunakan <, bukan >=
                mutation(child)

            new_population.append(child)

        generate_population = new_population

    result = max(generate_population, key=lambda schedule: hitung_fitness(schedule))
    return result


population = 50
generation = 100
mutation_probability = 0.2

result = geneticAlgo(population, generation, mutation_probability)

for i in result:
    for x in i:
        print(x.nama)
    print("\n")
