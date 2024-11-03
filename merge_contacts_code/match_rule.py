import re
import difflib
import csv
def get_dict(fname):
    row_set = set()
    with open(fname, mode='r', newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            row_tuple = tuple(row)
            row_set.add(row_tuple)
    
    return row_set

class MatchHandler:
    def __init__(self,successor=None) -> None:
        self.successor = successor
        self.matching = get_dict("matching.csv")
        self.no_matching = get_dict("no_matching.csv")
        
    def handle(self, valueA, valueB):
        if (valueB,valueA) in self.matching:
            return True
        if (valueB,valueA) in self.no_matching:
            return False
        valueA = re.sub(r'\s+|-','',valueA).lower()
        valueB = re.sub(r'\s+|-','', valueB).lower()
        handled = self.check_match(valueA, valueB)
        if not handled and self.successor:
            return self.successor.handle(valueA, valueB)
        return handled
    
    def check_match(self, valueA, valueB):
        raise NotImplemented("check match not implemented")

def salvos_store_match(value1, value2):
    tar = "salvosstore"
    if re.search(tar, value1) and re.search(tar, value2):
        v1 = re.sub(tar,'', value1)
        v2 = re.sub(tar,'',value2)
        #print(v1,' ',v2)
        if v1 == v2:
            return True
        
    return False

class BasicMatchHandler(MatchHandler):
    def check_match(self, valueA, valueB): 
        if valueA == valueB or salvos_store_match(valueA, valueB):
            return True
        else:
            return False
           

class DifflibMatchHandler(MatchHandler):
    def check_match(self, valueA, valueB, threshold=0.7):
       
        tar = "salvosstore"
        if re.search(r'salvosstore', valueA) or re.search(r'salvosstore', valueB):
            return False
        ratio = difflib.SequenceMatcher(None, valueA, valueB).ratio()
        return ratio >= threshold

    

handlerChain = BasicMatchHandler(DifflibMatchHandler())
# r = handlerChain.handle("salvos store AB","salvos store Abc")
# print(r)