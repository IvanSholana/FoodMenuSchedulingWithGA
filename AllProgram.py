import random


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


def initialize_chromosome(num_days):
    chromosome = []
    for _ in range(num_days):
        daily_menu = random.sample(ListMenu, 3)
        chromosome.extend(daily_menu)
    return chromosome


def hitung_fitness(gen):
    total_cost = sum(menu.harga for menu in gen)  # Jumlahkan total biaya
    penalti = 0

    # Cek Makanan Sama Kurang dari 3 Hari
    for i in range(3, len(gen), 3):
        daily_menus = set(gen[i - 3 : i])  # Periksa makanan yang berbeda dalam 3 hari
        if len(daily_menus) < 3:
            penalti += 3 - len(
                daily_menus
            )  # Gunakan 3 sebagai penalti karena ingin 3 makanan yang berbeda

    return 1 / (
        (total_cost / 3) + penalti
    )  # Bagi total_cost dengan 3 karena ingin total harga selama 3 hari


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
            if random.fl:  # Gunakan <, bukan >=
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
    print(i.nama)
