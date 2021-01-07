
import pandas as pd
from typing import List


class RoughSet:
    def __init__(self, U: pd.DataFrame, A: list):
        """
        An information system was defined as s = {U,A,V,f}.
        U: Objects
        A: Attributes
        V: Values by the mapping f function.
        f: Mapping function.
        classification: U/R. R is Attributes ,same as A. -> U/A
        """
        self.U = U # type: pd.DataFrame
        self.A = A # type: list
        self.classification = None  # U/A type: list
        """
        classification structure: set
        have to be a list (type set could not be recursive) # maybe need to extend set type.
        [element is instance of list or tuple]
        e.g. [[1],[2],[3,4]..] or [(1),(2,3)...]
        so as X
        """
        self.lower = None # type: list
        self.upper = None # type: list
        self._X = None # type: pd.DataFrame
        self._X_classification = None # type: list
        self.init()

    @staticmethod
    def flatten_list(l: list) -> list:
        r = []
        for e in l:
            if isinstance(e, list):
                r.extend(RoughSet.flatten_list(e))
            else:
                r.append(e)
        return r

    @staticmethod
    def card(l: list) -> int:
        """
        # cadinality
        """
        return len(RoughSet.flatten_list(l))

    @staticmethod
    def classify(U: pd.DataFrame, A: list) -> list:
        """
        classify
        generate classification = U/A
        A: Attributes
        """
        classification_index_list = []
        classification_grouped = U.groupby(by=A)
        for _, group_df in classification_grouped:
            classification_index_list.append(list(group_df.index))
        return classification_index_list

    def init(self):
        """
        for lazy load.
        get classification
        learn
        """
        self.classification = RoughSet.classify(self.U, self.A)
        return self


    @property
    def X(self) -> pd.DataFrame:
        return self._X

    @X.setter
    def X(self, X: pd.DataFrame):
        self._X = X

        classification = self.classification
        A = self.A
        self._X_classification = X_classification = RoughSet.classify(X, A)
        self.lower = self._get_lower(classification, X_classification)
        self.upper = self._get_upper(classification, X_classification)
        return self

    def _get_lower(self, classification: list, X_classification: list) -> List[list]:  # B_ lower boundary
        """
        lower index list.
        X classification: X classification,X group...
        """
        lower_index_list = []

        for k in classification:
            ks = set(k)
            for x in X_classification:
                xs = set(x)
                if ks.issubset(xs):
                    lower_index_list.append(k)
        return lower_index_list

    def _get_upper(self, classification: list, X_classification: list) -> List[list]:  # B-bar upper boundary
        """
        upper index list.
        X classification: X classification,X group...
        """
        upper_index_list = []

        for k in classification:
            ks = set(k)
            for x in X_classification:
                xs = set(x)
                if len(ks.intersection(xs)) != 0:
                    upper_index_list.append(k)

        return upper_index_list

    @property
    def bn(self) -> List[list]:
        """
        # boundary
        """
        upper = self.upper
        lower = self.lower
        upper_list = RoughSet.flatten_list(upper)
        lower_list = RoughSet.flatten_list(lower)
        bn_list = list(set(upper_list).difference(set(lower_list)))
        return bn_list

    @property
    def neg(self) -> List[list]:
        U = self.U
        upper = self.upper
        all_obj_set = set(U.index)
        neg = list(all_obj_set.difference(set(RoughSet.flatten_list(upper))))
        return neg

    @property
    def pos(self) -> List[list]:
        lower = self.lower
        return lower

    @property
    def alpha(self) -> float: # scale of rough
        return RoughSet.card(self.lower) / RoughSet.card(self.upper)

    def reduct(self):
        pass

    @property
    def core(self):
        pass

    def reducible(self, attrs: list) -> bool:   # check if reductible
        classification_list = self.classification
        A = self.A.copy()
        for a in attrs:
            A.remove(a)
        classification_new_list = RoughSet.classify(self.U, A)
        return RoughSet.compare_list(classification_list, classification_new_list)

    @staticmethod
    def list_to_set(l: list) -> List[list]:  # transform elements to set
        l2 = l.copy()  # use l will confuse the element (l was changing)
        for e in l:
            if isinstance(e, list):
                l2.remove(e)
                l2.append(set(e))
        return l2

    @staticmethod
    def compare_list(list1: list, list2: list) -> bool:  # for 2 level list [1,[1..]]
        """
        # check if list1 contains list2.
        """
        list1 = RoughSet.list_to_set(list1)
        list2 = RoughSet.list_to_set(list2)
        if len(list1) != len(list2):
            return False
        for e in list2:
            if e not in list1:
                return False
        return True
