from simple-dali import (
    MiniseedHeader,
    MiniseedRecord,
    unpackMiniseedHeader,
    unpackMiniseedRecord,
    unpackBlockette,
    MiniseedException,
)
from zipfile import ZipFile

from .quake_iterator import (
    QuakeIterator,
    FDSNQuakeIterator,
    QuakeMLFileIterator
    )
from .station_iterator import StationIterator, FDSNStationIterator
from .seismogram_iterator import (
    SeismogramIterator,
    FDSNSeismogramIterator,
    ThreeAtATime,
    CacheSeismogramIterator,
    )


DATASET_DIR = "dataset";
SEISMOGRAM_DIR = "seismograms";
CATALOG_FILE = "catalog.quakeml";
INVENTORY_FILE = "inventory.staxml";

def download_dataset(quake_query_params, station_query_params, seis_params):

    # Load stations, events and seismograms
    sta_itr = FDSNStationIterator(station_query_params, debug=debug)
    quake_itr = FDSNQuakeIterator(quake_query_params, debug=debug)
    print(f"Number of quakes: {len(quake_itr.quakes)}")

    # use ThreeAtATime to separate by band/inst code, ie seismometer then strong motion
    # at each station that has both
    seis_itr = ThreeAtATime(FDSNSeismogramIterator(quake_itr, sta_itr, debug=debug, **seis_params))

    with ZipFile('spam.zip', 'w') as myzip:
        myzip.mkdir(DATASET_DIR)
        with myzip.open(DATASET_DIR / INVENTORY_FILE, 'w') as invfile:
            sta_itr.inventory.write(invfile, format="STATIONXML")

        with myzip.open(DATASET_DIR / CATALOG_FILE, 'w') as catfile:
            quake_itr.quakes.write(catfile, format='QUAKEML')
        myzip.mkdir(SEISMOGRAM_DIR)
        net, sta, quake, seis = seis_itr.next()
        while sta is not None and quake is not None:
            if len(seis) != 0:
                time_str = calc_start(seis, quake).strftime("eq_%y-%m-%dT%H-%M-%S")
                seis_file = f"{net.networkCode}_{sta.stationCode}_{time_str}.ms3"
                index_num = 0
                while seis_file in myzip.namelist():
                    index_num += 1
                    seis_file = f"{net.networkCode}_{sta.stationCode}_{time_str}-{index_num}.ms3"
                with myzip.open(DATASET_DIR / seis_file, 'w') as seisfile:


def calc_start(stream, quake=None):
    if quake is not None and quake.preferred_origin() is not None:
        return quake.preferred_origin().time
    return min([trace.stats.starttime for trace in stream])

def trace_to_mseed3(trace):

    net_code = trace.stats.network
    sta_code = trace.stats.station
    loc_code = trace.stats.location
    chan_code = trace.stats.channel
    sid = FDSNSourceId.fromNslc(net_code, sta_code, loc_code, chan_code)
    ms3head = MSeed3Header(
        sid,
        trace.stats.starttime,
        len(trace),
        trace.stats
    )
