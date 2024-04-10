

class Listing:
    def __init__(self, address=None, price=None, area=None, roomNumber=None, floor=None, monthlyFee=None, sell_date=None):

        self.address = address
        self.price = price
        self.area = area
        self.roomNumber = roomNumber
        self.floor = floor
        self.monthlyFee = monthlyFee
        self.sell_date = sell_date

    def __str__(self):
        return f"Address: {self.address}\nPrice (Kr): {self.price}\nArea (m²): {self.area}\nNumber of rooms: {self.roomNumber}\nFloor: {self.floor}\nMonthly fee (Kr): {self.monthlyFee}\nSold on: {self.sell_date}"


class FilteringSettings:
    def __init__(self):

        self._address = None
        self._maxfee = None
        self._minrooms = None
        self._maxrooms = None
        self._minarea = None
        self._maxarea = None

    @property
    def address(self):
        return self._address

    @property
    def maxfee(self):
        return self._maxfee

    @property
    def maxrooms(self):
        return self._maxrooms

    @property
    def maxarea(self):
        return self._maxarea

    @property
    def minrooms(self):
        return self._minrooms

    @property
    def minarea(self):
        return self._minarea

    @address.setter
    def address(self, address):
        if address != '':
            self._address = address

    @maxfee.setter
    def maxfee(self, maxfee):
        if maxfee != '':
            self._maxfee = int(maxfee)

    @maxrooms.setter
    def maxrooms(self, maxrooms):
        if maxrooms != '':
            self._maxrooms = int(maxrooms)

    @maxarea.setter
    def maxarea(self, maxarea):
        if maxarea != '':
            self._maxarea = int(maxarea)

    @minrooms.setter
    def minrooms(self, minrooms):
        if minrooms != '':
            self._minrooms = int(minrooms)

    @minarea.setter
    def minarea(self, minarea):
        if minarea != '':
            self._minarea = int(minarea)

    def __str__(self):
        return f"Address: {self.address}\nMax monthly fee (Kr): {self.maxfee}\nMin rooms: {self.minrooms}\nMax rooms: {self.maxrooms}\nMin area (m²): {self.minarea}\nMax area (m²): {self.maxarea}\n"
