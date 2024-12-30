from itertools import chain
from random import seed, shuffle
from collections import defaultdict


def display_cards(cards, card_mapping):
    print("\t ", end='')
    print("\t ".join(f"{card_mapping[card]}" for card in cards))


base_unicode = {
    'hearts': 0x1F0B0,
    'diamonds': 0x1F0C0,
    'clubs': 0x1F0D0,
    'spades': 0x1F0A0
}

card_mapping = {-1: ""}

for i in range(14):
    if i < 11:
        card_mapping[i] = chr(base_unicode['hearts'] + (i + 1))
    elif i > 11:
        card_mapping[i - 1] = chr(base_unicode['hearts'] + (i + 1))

for i in range(14):
    if i < 11:
        card_mapping[13 + i] = chr(base_unicode['diamonds'] + (i + 1))
    elif i > 11:
        card_mapping[13 + i - 1] = chr(base_unicode['diamonds'] + (i + 1))

for i in range(14):
    if i < 11:
        card_mapping[26 + i] = chr(base_unicode['clubs'] + (i + 1))
    elif i > 11:
        card_mapping[26 + i - 1] = chr(base_unicode['clubs'] + (i + 1))

for i in range(14):
    if i < 11:
        card_mapping[39 + i] = chr(base_unicode['spades'] + (i + 1))
    elif i > 11:
        card_mapping[39 + i - 1] = chr(base_unicode['spades'] + (i + 1))



def simulate(n, i):
    from collections import defaultdict
    from random import shuffle, seed
    uncovered_count = defaultdict(int)
    for game in range(n):
        cards = list(range(52))
        pic = [10, 11, 12, 23, 24, 25, 36, 37, 38, 49, 50, 51]
        to_del = set()
        for r in range(4):
            if len(pic) == 0:
                break
            seed(i + game + r)
            shuffle(cards)
            cards = cards[::-1]
            idx = 16
            uncovered_cards = cards[:idx]
            uncovered_pictures = set(pic) & set(uncovered_cards)
            while len(uncovered_pictures) > 0:
                idx_replace = []
                card_to_replace = []
                for element in uncovered_pictures:
                    pic.remove(element)
                    to_del.add(element)
                    pos = uncovered_cards.index(element)
                    idx_replace.append(pos)
                    card_to_replace.append(cards[idx])
                    idx += 1
                idx_replace.sort()
                for j in range(len(idx_replace)):
                    uncovered_cards[idx_replace[j]] = card_to_replace[j]
                uncovered_pictures = set(pic) & set(uncovered_cards)
            cards = sorted(set(range(52)) - to_del)
        uncovered_count[len(to_del)] += 1
    card_data = dict(sorted(uncovered_count.items(), key=lambda x: x[0]))
    width = 40
    print(f"Number of uncovered pictures | Frequency")
    print(f"{'-' * width}")
    for uncovered_cnt, probability in card_data.items():
        probability = probability / n * 100
        if probability > 0:
            print(f"{uncovered_cnt:>28} | {probability:>8.2f}%")

if __name__ == "__main__":
    cards = list(range(52))
    s = int(input("Please enter an integer to feed the seed() function: "))
    pic = [10, 11, 12, 23, 24, 25, 36, 37, 38, 49, 50, 51]
    d = {1: "second", 2: "third", 3: "fourth"}
    to_del = set()
    for r in range(4):
        if len(pic) == 0:
            break
        seed(s + r)
        print()
        shuffle(cards)
        cards = cards[::-1]
        if r == 0:
            print("Deck shuffled, ready to start!")
            print(f"{']' * 52}")
            print()
            print("Starting first round...")
        else:
            print(f"After shuffling, starting {d[r]} round...")
        print()
        print(f"Drawing and placing 16 cards:")
        idx = 16
        print(f"{']' * (len(cards) - idx)}")
        uncovered_cards = cards[:idx]
        for i in range(4):
            display_cards(uncovered_cards[4 * i:4 * i + 4], card_mapping)

        uncovered_pictures = set(pic) & set(uncovered_cards)
        l, cnt = len(pic), 0
        while len(uncovered_pictures) > 0:
            print()
            idx_replace = []
            card_to_replace = []
            if len(uncovered_pictures) > 1:
                print(f"Putting {len(uncovered_pictures)} pictures aside:")
            else:
                print(f"Putting 1 picture aside:")
            for element in uncovered_pictures:
                pic.remove(element)
                to_del.add(element)
                pos = uncovered_cards.index(element)
                idx_replace.append(pos)
                card_to_replace.append(cards[idx])
                uncovered_cards[pos] = -1
                idx += 1
            idx_replace.sort()
            cnt = l - len(pic)
            l = len(pic)
            for i in range(4):
                display_cards(uncovered_cards[4 * i:4 * i + 4], card_mapping)
            if cnt > 0 and l != 0:
                print()
                if cnt > 1:
                    print(f"Drawing and placing {cnt} cards:")
                else:
                    print(f"Drawing and placing 1 card:")
                print(f"{']' * (len(cards) - idx)}")
                for i in range(len(idx_replace)):
                    uncovered_cards[idx_replace[i]] = card_to_replace[i]
                for i in range(4):
                    display_cards(uncovered_cards[4 * i:4 * i + 4], card_mapping)
            uncovered_pictures = set(pic) & set(uncovered_cards)
        cards = sorted(set(range(52)) - to_del)

    print()
    if len(pic) == 0:
        print("You uncovered all pictures, you won!")
    elif len(pic) == 12:
        print("You uncovered no pictures, you lost!")
    elif len(pic) == 11:
        print("You uncovered only 1 picture, you lost!")
    else:
        print(f"You uncovered only {12 - len(pic)} pictures, you lost!")

