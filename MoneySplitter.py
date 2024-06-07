# 出去玩算钱计算器
'''
event.add_transaction(spender=P.leo, cost_map={
        P.jayden: 15 + (6 + 4 + 5) / len(P),
        P.verona: 12 + (6 + 4 + 5) / len(P),
        P.charles: 15 + (6 + 4 + 5) / len(P),
        P.leo: 17 + (6 + 4 + 5) / len(P), 
        P.cheryl: (6 + 4 + 5) / len(P)
    }, amount=92.69, comment='mian')

event.add_transaction(spender=leo,   people=all, amount=30, comment='Gyubee')
'''
from collections.abc import Iterator
from enum import Enum

output = []
def _print(x):
    global output
    print(x)
    output.append(x)
    
def end(format=None):
    global output
    if format == None:
        with open(__file__, 'a') as f:
            f.write(f"\n\n'''\nOUTPUT\n" + '\n'.join(output) + "\n'''")
            pass
    elif type(format) == str:
        with open(format, 'w+') as f:
            f.write(f"\n\n'''\nOUTPUT\n" + '\n'.join(output) + "\n'''")
    else:
        print(f"\n\n'''\nOUTPUT\n" + '\n'.join(output) + "\n'''")

def exclude(all, exclude : list):
    out = all + []
    for p in exclude:
        out.remove(p)
    return out

class Transaction:
    def __init__(self, spender = "", people = [], amount = 0, comment = "", cost_map={}): 
        self.people = people
        self.amount = amount
        self.comment = comment
        self.spender = spender
        self.cost_map = cost_map

class Event:
    def __init__(self, people):
        self.people = {}
        self.spent = {}
        for p in people:
            self.people[p] = 0
            self.spent[p] = 0
        self.transactions = []
    
    def add_transaction(self, spender = "", people = [], amount = 0, comment = "", cost_map={}):
        if len(people) == 0 and cost_map == {}:
            raise Exception('Please properly indicate either people or cost_map')
        if len(set(people).union(set(self.people.keys()))) > len(self.people.keys()):
            print(people)
            raise Exception('Invalid people in events')
        self.transactions.append(Transaction(spender=spender, people=people, amount=amount, comment=comment, cost_map=cost_map))
    
    def calculate_summary(self):
        for t in self.transactions:
            if len(t.people) != 0:  # 平均分
                for p in t.people:
                    self.people[p] += t.amount / len(t.people)
            else:   # 百分比分摊
                total = sum(t.cost_map.values())
                for key in t.cost_map:
                    self.people[key] += t.amount / total * t.cost_map[key]
            self.spent[t.spender] += t.amount
            
        pos, neg = [], []
        
        _print("people\t\tshould spend\tspent\t\tdifference")
        for p in self.people:
            should_spend = round(self.people[p], 2)
            spent = round(self.spent[p], 2)
            diff = self.spent[p] - self.people[p]
            _print(f'{p}\t\t{should_spend}\t\t{spent}\t\t{round(spent - should_spend, 2)}')
            if diff > 0:
                pos.append([p, diff])
            elif diff < 0:
                neg.append([p, diff])
        assert round(sum([x[1] for x in pos]) + sum([x[1] for x in neg]), 3) == 0
        
        get_diff = lambda x: x[1]
        pos.sort(key=get_diff, reverse=True)
        neg.sort(key=get_diff, reverse=True)
        # print(pos)
        # print(neg)
        
        _print("\n")
        while len(pos) != 0 and len(neg) != 0:
            # print(pos)
            # print(neg)
            if pos[0][1] + neg[0][1] > 0:
                _print(f'{neg[0][0]} give {pos[0][0]} ${round(abs(neg[0][1]), 2)}')
                pos[0][1] += neg[0][1]
                neg.pop(0)
            else:
                _print(f'{neg[0][0]} give {pos[0][0]} ${round(abs(pos[0][1]), 2)}')
                neg[0][1] += pos[0][1]
                pos.pop(0)
    
            
    def print_transactions(self):
        pass

class P(Enum):
    leo = "leo"
    charles = "charles"
    verona = "verona"
    cheryl = "cheryl"
    jayden = "jayden"
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value
    
    def all():
        return [P.leo, P.charles, P.verona, P.cheryl, P.jayden]

    def __len__(self) -> int:
        return super().__len__()
                    
if __name__ == "__main__":
    event = Event(P.all())

    # event.add_transaction(spender=, people=, amount=, comment='')
    event.add_transaction(spender=P.leo, cost_map={
        P.jayden: 15 + (6 + 4 + 5) / len(P),
        P.verona: 12 + (6 + 4 + 5) / len(P),
        P.charles: 15 + (6 + 4 + 5) / len(P),
        P.leo: 17 + (6 + 4 + 5) / len(P), 
        P.cheryl: (6 + 4 + 5) / len(P)
    }, amount=92.69, comment='mian')
    event.calculate_summary()
    end()
'''
OUTPUT
people		should spend	spent		difference
leo		25.05		92.69		67.64
charles		22.55		0		-22.55
verona		18.79		0		-18.79
cheryl		3.76		0		-3.76
jayden		22.55		0		-22.55


cheryl give leo $3.76
verona give leo $18.79
charles give leo $22.55
jayden give leo $22.55
'''
