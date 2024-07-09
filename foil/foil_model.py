from abc import abstractmethod
import statistics
from .foil_types import *

class FoilBase:
    def __init__(self, f_FOIL, f_Label) -> None:
        self._rules: FoilRules = {}
        self._object_list = []
        self._initialized = False
        self._FOIL = f_FOIL
        self._Label = f_Label

    def get_rules(self) -> FoilRules:
        if not self._initialized:
            print("Please fit the model first.")
            return
        return self._rules

    def set_rules(self, new_rule: str) -> None:
        import json
        try:
            if isinstance(new_rule, str):
                self._rules = json.loads(new_rule)
            else:
                self._rules = new_rule
        except:
            print("Please input a valid json or string.")
            return

    def get_object_list(self) -> list[str]:
        if not self._initialized:
            print("Please fit the model first.")
            return
        return self._object_list

    def print_rules(self):
        if not self._initialized:
            print("Please fit the model first.")
            return
        print("Current Rules:")
        for idx, (k, v) in enumerate(self._rules.items()):
            print(f"Rule {idx}({k.split('(')[0]}): {v}")
        print("End")
    
    def print_object_list(self):
        if not self._initialized:
            print("Please fit the model first.")
            return
        print("Current Object List:")
        for idx, obj in enumerate(self._object_list):
            print(f"{idx}: {obj}")
        print("End")

    @abstractmethod
    def fit(self, X: FoilX, y: Foily, d, l) -> None:
        raise NotImplementedError("Method not implemented or directly call in FoilBase.")

    @abstractmethod
    def predict(self, X: FoilX, **kwargs) -> list[list[str]]:
        raise NotImplementedError("Method not implemented or directly call in FoilBase.")

    @abstractmethod
    def score(self, X: FoilX, y: Foily):
        raise NotImplementedError("Method not implemented or directly call in FoilBase.")

    @abstractmethod
    def predict_proba(self, X: FoilX):
        raise NotImplementedError("Method not implemented or directly call in FoilBase.")
    

class FoilImageClassifier(FoilBase):
    def __init__(self, f_FOIL, f_LABEL) -> None:
        super().__init__(f_FOIL, f_LABEL)
        self.max_acc = -1
        self.max_rules: FoilRules = {}

    @staticmethod
    def parse_data(image_meta_data, interpretation, isManual=True) -> FoilXItem:
        X: FoilXItem = {
            "imageId": image_meta_data['imageId'],
        }
        for key, value in interpretation.items():
            X[key] = value
        if(isManual):
            y = image_meta_data['labels'][0]['name'][0]
        else:
            y = None
        return X, y

    def get_max_acc(self):
        return self.max_acc

    def get_max_rules(self):
        return self.max_rules

    def fit(self, X: FoilX, y: Foily, d={}, l={}) -> None:
        combined_input = X.copy()
        for i in range(len(combined_input)):
            combined_input[i]['type'] = y[i]
        # print("Start running FOIL algo...")
        result = self._FOIL(input_list=combined_input, deleted=d, locked=l)
        # print("FOIL finished...")
        self._rules = result[0]
        self._object_list = result[2]
        self._initialized = True
        return

    def predict(self, X: FoilX, **kwargs) -> list[list[str]]:
        if not self._initialized:
            print("Please fit the model first.")
            return
        # Can show the rules here
        result, satis_list = self._Label(dict_list=X, rules=self._rules)
        # drop '(X)'
        for l in result:
            for i in range(len(l)):
                l[i] = l[i].split('(')[0]
        
        if 'rt_satis_list' in kwargs and kwargs['rt_satis_list']:
            return result, satis_list
        return result

    def score(self, X: FoilX, y: Foily, max_track=True):
        if not self._initialized:
            print("Please fit the model first.")
            return
        result = self.predict(X)
        # print(result[0:10])
        correct = 0
        total = 0
        for idx, l in enumerate(result):
            total += 1
            if len(l) == 1 and l[0].strip() == y[idx].strip():
                correct += 1

        acc = correct / total
        if max_track and acc > self.max_acc:
            self.max_acc = acc
            self.max_rules = self._rules
        return acc

    def predict_proba(self, X: FoilX):
        if not self._initialized:
            print("Please fit the model first.")
            return
        label_result = self._Label(dict_list=X, rules=self._rules)
        # calculate probability based on list length
        result = []
        for l in label_result: 
            list_len = len(l)
            prob = 1 / list_len
            result.append(prob)
        return result