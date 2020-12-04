
import pandas as pd


class Roughset:
    def __init__(self, U: pd.DataFrame, A: list):
        """
        An information system was defined as s = {U,A,V,f}.
        U: Objects
        A: Attributes
        V: Values by the mapping f function.
        f: Mapping function.
        classcification: U/R. R is relationship ,same as A. -> U/A
        """
        self.U = U # type: pd.DataFrame
        self.A = A # type: list
        self.classcification = None  # U/A type: list
        """
        classcification structure: set
        have to be a list (type set could not be recursive) # maybe need to extend set type.
        [element is instance of list or tuple]
        e.g. [[1],[2],[3,4]..] or [(1),(2,3)...]
        so as X
        """
        self.lower = None # type: list
        self.upper = None # type: list
        self.bn = None  # boundary
        self.pos = None # type: list
        self.neg = None # type: list
        self.X = None # type: pd.DataFrame
        self._X_classcification = None # type: list
        self.core = None # type: list
        self.init()

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
    def get_classcification(U: pd.DataFrame, A: list) -> list:
        """
        classify
        generate classcification = U/A
        A: Attributes
        """
        classcification_index_list = []
        classcification_grouped = U.groupby(by=A)
        for _, group_df in classcification_grouped:
            classcification_index_list.append(list(group_df.index))
        return classcification_index_list

    def init(self) -> list:
        """
        for lazy load.
        get classcification
        learn
        """
        self.classcification = Roughset.get_classcification(self.U, self.A)
        return self

    def set_X(self, X: pd.DataFrame):
        self.X = X
        classcification = self.classcification
        A = self.A
        self._X_classcification = X_classification = Roughset.get_classcification(X, A)
        self.lower = self._get_lower(classcification, X_classification)
        self.upper = self._get_upper(classcification, X_classification)
        self.bn = self.__get_bn(self.upper, self.lower)
        self.pos = self.__get_pos(self.lower)
        self.neg = self.__get_neg(self.U, self.upper)
        return self

    def _get_lower(self, classcification: list, X_classification: list) -> list:  # B_ lower boundary
        """
        lower index list.
        X classification: X classcification,X group...
        """
        lower_index_list = []

        for k in classcification:
            ks = set(k)
            for x in X_classification:
                xs = set(x)
                if ks.issubset(xs):
                    lower_index_list.append(k)
        return lower_index_list

    def _get_upper(self, classcification: list, X_classification: list) -> list:  # B-bar upper boundary
        """
        upper index list.
        X classification: X classcification,X group...
        """
        upper_index_list = []

        for k in classcification:
            ks = set(k)
            for x in X_classification:
                xs = set(x)
                if len(ks.intersection(xs)) != 0:
                    upper_index_list.append(k)

        return upper_index_list

    def __get_bn(self, upper: list, lower: list) -> list:
        upper_list = Roughset.flatten_list(upper)
        lower_list = Roughset.flatten_list(lower)
        bn_list = list(set(upper_list).difference(set(lower_list)))
        return bn_list

    def __get_neg(self, U: pd.DataFrame , upper:list) -> list:
        all_obj_set = set(U.index)
        neg = list(all_obj_set.difference(set(Roughset.flatten_list(upper))))
        return neg

    def __get_pos(self, lower: list) -> list:
        return lower


    def alpha(self):  # scale of rough
        return Roughset.card(self.lower) / Roughset.card(self.upper)

    def reduct(self):
        pass

    def core(self):
        pass

    def reducible(self, attrs: list):  # check if reductible
        classcification_list = self.classcification
        A = self.A.copy()
        for a in attrs:
            A.remove(a)
        classcification_new_list = Roughset.get_classcification(self.U, A)
        return Roughset.compare_list(classcification_list, classcification_new_list)

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
