from moneymoney.currency_codes import CurrencyCodes


class CurrencyCodeIsNoneException(Exception):
    """Exception thrown when CurrencyCode is None."""


class CurrencyIsNotTheSameException(Exception):
    """Exception thrown when currencies are different."""


class Money:
    """Class representing an amount with a currency.

    Money of different currency cannot operate between them, they need
    to be of the same currency.
    """

    def __init__(self, currency_code: str, amount: float = 0.0):
        if currency_code is None:
            raise CurrencyCodeIsNoneException()
        self._amount = amount
        self._currency_code = currency_code

    @property
    def amount(self) -> float:
        """Property amount of this object."""
        return self._amount

    @property
    def currency_code(self):
        """Property currency_code of this object."""
        return self._currency_code

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency_code.lower() != self.currency_code.lower():
                raise CurrencyIsNotTheSameException()
            other = other.amount
        amount = self.amount + other
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency_code.lower() != self.currency_code.lower():
                raise CurrencyIsNotTheSameException()
            other = other.amount
        amount = self.amount - other
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __eq__(self, other):
        if isinstance(other, Money):
            return (self._amount == other.amount) and (self._currency_code.lower() == other.currency_code.lower())
        return False

    def __str__(self):
        rounded_amount = round(self.amount, 2)
        return f"{rounded_amount}{self.currency_code}"


DEFAULT_MONEY = Money(currency_code=CurrencyCodes.EUR)
