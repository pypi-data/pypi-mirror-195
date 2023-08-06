from abc import ABC, abstractmethod
from obspy.clients.fdsn import Client
from obspy import Inventory, read_inventory
from obspy.clients.fdsn.header import FDSNNoDataException


class StationIterator(ABC):
    def __init__(self):
        self.__empty__ = None, None
    @abstractmethod
    def next(self):
        return self.__empty__
    @abstractmethod
    def prev(self):
        return self.__empty__
    def beginning(self):
        pass
    def ending(self):
        pass

class StationXMLIterator(StationIterator):
    def __init__(self, inv, debug=False):
        self.debug = debug
        self.__empty__ = None, None
        self.net_idx = 0
        self.sta_idx = -1
        self.inv = inv
    def current(self):
        return self.inv.networks[self.net_idx], self.inv.networks[self.net_idx].stations[self.sta_idx]
    def next(self):
        self.sta_idx += 1
        if self.net_idx >= len(self.inv.networks):
            return self.__empty__
        while self.sta_idx >= len(self.inv.networks[self.net_idx].stations):
            self.net_idx += 1
            self.sta_idx = 0
            if self.net_idx >= len(self.inv.networks):
                return self.__empty__
        return self.inv.networks[self.net_idx], self.inv.networks[self.net_idx].stations[self.sta_idx]
    def prev(self):
        self.sta_idx -= 1
        while self.sta_idx < 0:
            self.net_idx -= 1
            if self.net_idx < 0:
                return self.__empty__
            self.sta_idx = len(self.inv.networks[self.net_idx].stations)-1
        return self.inv.networks[self.net_idx], self.inv.networks[self.net_idx].stations[self.sta_idx]
    def beginning(self):
        self.net_idx = 0
        self.sta_idx = -1
    def ending(self):
        self.net_idx = len(self.inv.networks)-1
        self.sta_idx = len(self.inv.networks[self.net_idx])
    def __len__(self):
        count = 0
        for n in self.inv.networks:
            count += len(n.stations)
        return count


class StationXMLFileIterator(StationXMLIterator):
    def __init__(self, filename):
        super().__init__(read_inventory(filename))

class FDSNStationIterator(StationXMLIterator):
    def __init__(self, query_params, dc_name="IRIS", debug=False):
        self.debug = debug
        self.__empty__ = None, None
        self.dc_name = dc_name
        self.query_params = dict(query_params)
        if "level" not in query_params:
            self.query_params["level"] = "channel"
        super().__init__(self.__load__())

    def __load__(self):
        try:
            client = Client(self.dc_name, _discover_services=False, debug=self.debug)
            return client.get_stations(**self.query_params)
        except FDSNNoDataException:
            return Inventory()
