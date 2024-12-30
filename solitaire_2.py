from itertools import chain
from random import seed, shuffle
from collections import defaultdict

base_unicode = {
    'hearts': 0x1F0B0,
    'diamonds': 0x1F0C0,
    'clubs': 0x1F0D0,
    'spades': 0x1F0A0
}

card_mapping = {}

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
mapping_card = {v:k for k,v in card_mapping.items()}

def canPut(card,line1,line2,line3,line4,output,to_del):
    Aces = [0,13,26,39]
    Kings = [12,25,38,51]
    flag = 0
    if(card in Aces or card in Kings):
        output.append("Placing one of the base cards!")
        output.append(line1)
        line2.pop()
        l = len(line2)
        if l > 0:
            new_line2 = ["[" for _ in range(l - 1)]
            new_line2.append(card_mapping[line2[-1]])
        else:
            new_line2 = ""
        output.append("".join(new_line2))
        if card in Aces:
            p = Aces.index(card)*15
            line3[p] = card_mapping[card]
        else:
            p = Kings.index(card)*15
            line4[p] = card_mapping[card]
        if line3.count(" ") != 60 and line4.count(" ") != 60:
            output.append(("    " + "".join(line3)).rstrip())
            output.append(("    " + "".join(line4)).rstrip())
        elif line3.count(" ") != 60 and line4.count(" ") == 60:
            output.append(("    " + "".join(line3)).rstrip())
            output.append("")
        elif line3.count(" ") == 60 and line4.count(" ") != 60:
            output.append("")
            output.append(("    " + "".join(line4)).rstrip())
        else:
            output.append("")
            output.append("")
        output.append("")
        to_del.add(card)
        return True
    else:
        if 0 < card < 12:
            i, j = 0, 0
        elif 13 < card < 25:
            i,j = 15,15
        elif 26 < card < 38:
            i, j = 30, 30
        elif 39 < card < 51:
            i, j = 45, 45
        valid_line3, valid_line4 = [], []
        while line3[i] != ' ':
            valid_line3.append(line3[i])
            i += 1
        while line4[j] != ' ':
            valid_line4.append(line4[j])
            j += 1
        if len(valid_line3) and card == mapping_card[valid_line3[-1]] + 1:
            flag = 1
            output.append("Making progress on an increasing sequence!")
            line3[i] = card_mapping[card]
            line3[i - 1] = '['
        elif len(valid_line4) and card == mapping_card[valid_line4[-1]] - 1:
            flag = 1
            output.append("Making progress on a decreasing sequence!")
            line4[j] = card_mapping[card]
            line4[j - 1] = '['
        if flag == 1:
            output.append(line1)
            line2.pop()
            l = len(line2)
            if l > 0:
                new_line2 = ["[" for _ in range(l - 1)]
                new_line2.append(card_mapping[line2[-1]])
            else:
                new_line2 = ""
            output.append("".join(new_line2))
            if line3.count(" ") != 60 and line4.count(" ") != 60:
                output.append(("    " + "".join(line3)).rstrip())
                output.append(("    " + "".join(line4)).rstrip())
            elif line3.count(" ") != 60 and line4.count(" ") == 60:
                output.append(("    " + "".join(line3)).rstrip())
                output.append("")
            elif line3.count(" ") == 60 and line4.count(" ") != 60:
                output.append("")
                output.append(("    " + "".join(line4)).rstrip())
            else:
                output.append("")
                output.append("")
            output.append("")
            to_del.add(card)
            return True
        return False

def input_check(op,length):
    if "--" in op:
        parts = op.split("--")
        if len(parts) != 2:
            return False,[]
        try:
            m,n = int(parts[0]),int(parts[1])
            if 1 <= m <= n <= length:
                return True,[m,n]
            else:
                raise ValueError
        except ValueError:
            return False,[]
    else:
        if "+" in op:
            return False,[]
        try:
            num = int(op)
            if 1 <= num <= length or 0-length <= num <= -1:
                return True,[num]
        except ValueError:
            return False,[]


def simulate(n,i):
    left_count = defaultdict(int)
    for game in range(n):
        to_del = set()
        round_cnt = 0
        line3, line4 = [" " for _ in range(60)], [" " for _ in range(60)]
        output = []
        last_del = set()
        cards = list(range(52))
        seed(i+game)
        shuffle(cards)
        cards = cards[::-1]
        while len(cards):
            if to_del == last_del and round_cnt != 0:
                break
            last_del = to_del.copy()
            round_cnt += 1
            line1, line2, = f"{']' * len(cards)}", []
            idx = 0
            cnt = 0
            while len(line1):
                if len(line1) > 3:
                    line1 = line1[3:]
                    idx += 3
                    line2 = cards[:idx - cnt]
                else:
                    line1 = ""
                    line2 = cards.copy()
                curr_cards = line2.copy()
                while curr_cards and canPut(curr_cards[-1], line1, line2, line3, line4, output, to_del):
                    number = curr_cards[-1]
                    pos = cards.index(number)
                    cards.pop(pos)
                    cnt += 1
                    curr_cards.pop(-1)
            cards = line2
        left_count[len(cards)] += 1
    card_data = dict(sorted(left_count.items(), key=lambda x: x[0],reverse=True))
    width = 32
    print(f"Number of cards left | Frequency")
    print(f"{'-' * width}")
    for left_cnt, probability in card_data.items():
        probability = probability / n * 100
        if probability > 0:
            print(f"{left_cnt:>20} | {probability:>8.2f}%")


if __name__ == "__main__":
    cards = list(range(52))
    s = int(input("Please enter an integer to feed the seed() function: "))
    d = {0:"first",1: "second", 2: "third",}
    to_del = set()
    round_cnt = 0
    output = ["Deck shuffled, ready to start!", f"{']'*52}",""]
    last_len = 52
    last_del = set()
    line3, line4 = [" " for _ in range(60)],[" " for _ in range(60)]
    seed(s)
    shuffle(cards)
    cards = cards[::-1]
    while len(cards):
        if to_del == last_del and round_cnt != 0:
            break
        last_del = to_del.copy()
        last_len = len(cards)
        if round_cnt < 3:
            output.append(f"Starting to draw 3 cards (if possible) again and again for the {d[round_cnt]} time...")
            output.append("")
        else:
            output.append(f"Starting to draw 3 cards (if possible) again and again for the {round_cnt+1}th time...")
            output.append("")
        round_cnt += 1
        line1, line2,  = f"{']' * len(cards)}",[]

        idx = 0
        cnt = 0
        while len(line1):
            if len(line1) > 3:
                line1 = line1[3:]
                idx += 3
                line2 = cards[:idx-cnt]
            else:
                line1 = ""
                line2 = cards.copy()
            l = len(line2)
            new_line2 = ["[" for _ in range(l - 1)]
            new_line2.append(card_mapping[line2[-1]])
            output.append(line1)
            output.append("".join(new_line2))
            if line3.count(" ") != 60 and line4.count(" ") != 60:
                output.append(("    "+"".join(line3)).rstrip())
                output.append(("    "+"".join(line4)).rstrip())
            elif line3.count(" ") != 60 and line4.count(" ") == 60:
                output.append(("    "+"".join(line3)).rstrip())
                output.append("")
            elif line3.count(" ") == 60 and line4.count(" ") != 60:
                output.append("")
                output.append(("    "+"".join(line4)).rstrip())
            else:
                output.append("")
                output.append("")
            output.append("")
            curr_cards = line2.copy()
            while curr_cards and canPut(curr_cards[-1],line1,line2,line3,line4,output,to_del):
                n = curr_cards[-1]
                pos = cards.index(n)
                cards.pop(pos)
                cnt += 1
                curr_cards.pop(-1)
        cards = line2
    output.pop()
    if not cards:
        print()
        print("All cards have been placed, you won!")
        print()
    else:
        print()
        print(f"{len(cards)} cards could not be placed, you lost!")
        print()
    print(f"There are {len(output)} lines of output; what do you want me to do?")
    print()
    op = input(f"Enter: q to quit\n \
      a last line number (between 1 and {len(output)})\n \
      a first line number (between -1 and -{len(output)})\n \
      a range of line numbers (of the form m--n with 1 <= m <= n <= {len(output)})\n \
      ")
    print()
    while op != 'q':
        flag,res = input_check(op,len(output))
        if not flag:
            op = input(f"Enter: q to quit\n \
      a last line number (between 1 and {len(output)})\n \
      a first line number (between -1 and -{len(output)})\n \
      a range of line numbers (of the form m--n with 1 <= m <= n <= {len(output)})\n \
      ")
            if op == 'q':
                break
            print()
        else:
            if len(res) == 2:
                m,n = res[0],res[1]
                for i in range(m,n+1):
                    print(output[i-1])
            elif len(res) == 1:
                num = res[0]
                if num > 0:
                    for i in range(1, num + 1):
                        print(output[i - 1])
                else:
                    for i in range(num,0):
                        print(output[i])
            print()
            op = input(f"Enter: q to quit\n \
      a last line number (between 1 and {len(output)})\n \
      a first line number (between -1 and -{len(output)})\n \
      a range of line numbers (of the form m--n with 1 <= m <= n <= {len(output)})\n \
      ")
            if op == 'q':
                break
            print()





