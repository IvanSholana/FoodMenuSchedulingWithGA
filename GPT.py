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


# Menu Makanan tetap sama
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
    random.shuffle(child)


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

    return 1 / (total_cost + penalti)


def geneticAlgo(population, generation, mutation_probability):
    generate_population = [initialize_chromosome(30) for _ in range(population)]

    for gen in range(generation):
        fitness_scores = [hitung_fitness(chrom) for chrom in generate_population]
        best_fitness = max(fitness_scores)
        print(f"Generasi {gen + 1}, Fitness Terbaik: {best_fitness}")

        # Ambil 10% kromosom dengan nilai fitness tertinggi sebagai induk
        num_parents = int(population * 0.1)
        selected_parents = sorted(
            generate_population, key=hitung_fitness, reverse=True
        )[:num_parents]

        new_population = selected_parents[:]  # Jadikan kromosom terbaik sebagai induk

        while len(new_population) < population:
            parent1 = random.choice(selected_parents)
            parent2 = random.choice(selected_parents)

            child = crossover(parent1, parent2)
            if random.random() < mutation_probability:
                mutation(child)

            new_population.append(child)

        generate_population = new_population

    # Ambil kromosom terbaik dari populasi terakhir sebagai hasil akhir
    best_chrom = max(generate_population, key=hitung_fitness)
    return best_chrom


population = 50
generation = 500
mutation_probability = 0.2

best_schedule = geneticAlgo(population, generation, mutation_probability)

# Outputkan hasil jadwal terbaik
total_cost = 0
for i in best_schedule:
    for x in i:
        print(x.nama)
        total_cost += x.harga
    print("")
print(total_cost)
