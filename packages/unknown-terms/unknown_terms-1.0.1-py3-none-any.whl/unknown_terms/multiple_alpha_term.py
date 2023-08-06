class MultipleAlphaTerm:
    def __init__(self, _terms: list):
        self.terms: list = _terms
        self.__coefficient = self.get_coefficient()
        self.seperated_terms = self.seperate_by_alphas()

    def set_coefficient(self, value):
        self.__coefficient = value

    def get_coefficient(self):
        result = 1
        for term in self.terms:
            result *= term.get_coefficient()

        return result

    @staticmethod
    def __multiply_alpha_bros(terms) -> 'AlphaTerm':
        result = terms[0]
        for term in terms[1:]:
            result *= term
        return result

    def seperate_by_alphas(self) -> list:
        terms_dict = dict()
        for _term in self.terms:
            if not terms_dict.get(_term.get_alpha()):
                terms_dict[_term.get_alpha()] = list()
            terms_dict[_term.get_alpha()].append(_term)

        for alpha in terms_dict.keys():
            if len(terms_dict[alpha]) > 1:
                terms_dict[alpha] = [self.__multiply_alpha_bros(terms_dict[alpha])]

        final_terms = []
        for t in terms_dict.values():
            final_terms.append(t[0])
        return final_terms

    def get_full_term(self) -> str:
        alpha_exp = ""

        for term in self.seperated_terms:
            alpha_exp += term.get_alpha() + term.get_printable_exponent()

        return str(self.get_coefficient()) + alpha_exp

    def get_derivative(self, _d: str, degree=1):
        terms = self.terms.copy()

        for index, term in enumerate(terms):
            if term.get_alpha() == _d:
                derrived_term = term.get_derivative(degree)
                if derrived_term == 0:
                    return 0
                else:
                    terms[index] = derrived_term
                    continue

        if self.terms == terms:
            raise ValueError("You can't derive from a variable that doesn't exist.")
        else:
            return MultipleAlphaTerm(terms)

    def turn_to_known(self, **values):
        new_term = self.__copy__()
        new_alpha_term = self.terms[0].__copy__()

        for term in self.seperated_terms:
            value = values.get(term.get_alpha())

            if value:
                try:
                    new_term.__coefficient /= term.get_coefficient()
                except ZeroDivisionError:
                    pass
                new_term.__coefficient *= term.turn_to_known(value)
                new_term.seperated_terms.remove(term)

            if len(new_term.seperated_terms) == 1:
                if new_term.seperated_terms[0].get_alpha() in values.keys():
                    continue
                else:
                    new_alpha_term.set_coefficient(new_term.__coefficient)
                    new_alpha_term.set_alpha(new_term.seperated_terms[0].get_alpha())
                    new_alpha_term.set_exponent(new_term.seperated_terms[0].get_exponent())
                    return new_alpha_term
            elif len(new_term.seperated_terms) == 0:
                return new_term.get_coefficient()
            else:
                if set(values).intersection(set([t.get_alpha() for t in new_term.seperated_terms])):
                    continue
                else:
                    return new_term

    def __str__(self) -> str:
        return self.get_full_term()

    def __mul__(self, other) -> 'MultipleAlphaTerm':
        if isinstance(other, int) or isinstance(other, float):
            new_terms = self.terms.copy()
            new_terms[-1] = new_terms[-1].__copy__() * other
            return MultipleAlphaTerm(new_terms)
        elif isinstance(other, type(self.terms[-1])):  # self.terms[-1] always will be an AlphaTerm object.
            new_terms = self.terms + [other]
            return MultipleAlphaTerm(new_terms)
        elif isinstance(other, type(self)):
            new_terms = self.terms + other.terms
            return MultipleAlphaTerm(new_terms)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __copy__(self):
        return MultipleAlphaTerm(self.terms)

    def __pow__(self, power):
        new_terms = []
        for term in self.seperated_terms:
            new_terms.append(term ** power)

        return MultipleAlphaTerm(new_terms)

    def __truediv__(self, other):
        if type(other) in [int, float]:
            if other == 0:
                raise ValueError("MultipleAlphaTerm object cannot be divided by zero")
            return self.__mul__(1 / other)
        elif isinstance(other, type(self.terms[-1])):
            if other.is_equal_zero:
                raise ValueError("MultipleAlphaTerm object cannot be divided by zero")
            else:
                new_object = other.__copy__()
                new_object.set_coefficient(1 / other.get_coefficient())
                new_object.set_exponent(-other.get_exponent())
            return MultipleAlphaTerm(self.terms + [new_object])
        elif isinstance(other, type(self)):
            other_terms = []
            for term in other.terms:
                new_term = term.__copy__()
                new_term.set_coefficient(1 / term.get_coefficient())
                new_term.set_exponent(-term.get_exponent)
                other_terms.append(new_term)

            return MultipleAlphaTerm(self.terms + [other_terms])

    def __float__(self):
        return float(self.__coefficient)

    def __abs__(self):
        new_term = MultipleAlphaTerm(self.terms)
        new_term.__coefficient = abs(new_term.get_coefficient())
        new_term.set_coefficient(abs(self.get_coefficient()))
        return new_term
