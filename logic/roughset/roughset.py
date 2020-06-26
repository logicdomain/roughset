
import pandas as pd


class Roughset:
    def __init__(self, U: pd.DataFrame, A: list):
        """
        An information system was defined as s = {U,A,V,f}.
        U: Objects
        A: Attributes
        V: Values by the mapping f function.
        f: Mapping function.
        knowledge: U/R. R is relationship ,same as A. -> U/A
        """
        self.U = U
        self.A = A
        self.knowledge = None  # U/A list
        """
        knowledge structure: set
        have to be a list (type set could not be recursive) # maybe need to extend set type.
        [element is instance of list or tuple]
        e.g. [[1],[2],[3,4]..] or [(1),(2,3)...]
        so as X
        """
        self.lower = None
        self.upper = None
        self.bn = None  # boundary
        self.X = None
        self._X_knowledge = None
        self.core = None

    @staticmethod
    def flatten_list(l: list) -> list:
        r = []
        for e in l:
            if isinstance(e, list):
                r.extend(Roughset.flatten_list(e))
            else:
                r.append(e)
        return r

    @staticmethod
    def card(l: list) -> float:
        return len(Roughset.flatten_list(l))

    @staticmethod
    def get_knowledge(U: pd.DataFrame, A: list) -> list:
        """
        classify
        generate knowledge = U/A
        A: Attributes
        """
        knowledge_index_list = []
        knowledge_grouped = U.groupby(by=A)
        for _, group_df in knowledge_grouped:
            knowledge_index_list.append(list(group_df.index))
        return knowledge_index_list

    def init(self) -> list:
        """
        for lazy load.
        get knowledge
        learn
        """
        self.knowledge = Roughset.get_knowledge(self.U, self.A)
        return self

    def set_X(self, X: pd.DataFrame):
        self.X = X
        knowledge = self.knowledge
        A = self.A
        self._X_knowledge = X_classification = Roughset.get_knowledge(X, A)
        self._get_lower(knowledge, X_classification)
        self._get_upper(knowledge, X_classification)
        return self

    def _get_lower(self, knowledge: list, X_classification: list) -> list:  # B_ lower boundary
        """
        lower index list.
        X classification: X knowledge,X group...
        """
        lower_index_list = []

        for k in knowledge:
            ks = set(k)
            for x in X_classification:
                xs = set(x)
                if ks.issubset(xs):
                    lower_index_list.append(k)
        self.lower = lower_index_list
        return lower_index_list

    def _get_upper(self, knowledge: list, X_classification: list) -> list:  # B-bar upper boundary
        """
        upper index list.
        X classification: X knowledge,X group...
        """
        upper_index_list = []

        for k in knowledge:
            ks = set(k)
            for x in X_classification:
                xs = set(x)
                if len(ks.intersection(xs)) != 0:
                    upper_index_list.append(k)

        self.upper = upper_index_list
        return upper_index_list

    def alpha(self):  # scale of rough
        return Roughset.card(self.lower) / Roughset.card(self.upper)

    def reduct(self):
        pass

    def core(self):
        pass

    def reducible(self, attrs: list):  # check if reductible
        knowledge_list = self.knowledge
        A = self.A.copy()
        for a in attrs:
            A.remove(a)
        knowledge_new_list = Roughset.get_knowledge(self.U, A)
        return Roughset.compare_list(knowledge_list, knowledge_new_list)

    @staticmethod
    def trans_to_set(l: list) -> list:  # transform elements to set
        l2 = l.copy()  # use l will confuse the element (l was changing)
        for e in l:
            if isinstance(e, list):
                l2.remove(e)
                l2.append(set(e))
        return l2

    @staticmethod
    def compare_list(list1: list, list2: list):  # for 2 level list [1,[1..]]
        list1 = Roughset.trans_to_set(list1)
        list2 = Roughset.trans_to_set(list2)
        if len(list1) != len(list2):
            return False
        for e in list2:
            if e not in list1:
                return False
        return True
