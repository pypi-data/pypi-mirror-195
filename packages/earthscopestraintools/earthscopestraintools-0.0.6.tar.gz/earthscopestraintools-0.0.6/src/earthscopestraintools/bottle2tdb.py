from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from earthscopestraintools.bottletar import GtsmBottleTar
import tiledb
from earthscopestraintools.tiledbtools import StrainArray, RawStrainWriter
from earthscopestraintools.edid import get_station_edid, get_session_edid
import logging

# from straintiledbarray import StrainTiledbArray, Writer
logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.setLevel(logging.INFO)
else:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )


def build_strain_buffer(gbt: GtsmBottleTar, session: str):
    logger.info(
        f"{gbt.file_metadata['filename']}: loading strain bottles into dataframe"
    )
    bottle_dfs = []
    logger.info(
        f"{gbt.file_metadata['filename']}: contains {len(gbt.bottle_list)} bottle files"
    )
    for i, name in enumerate(gbt.bottle_list):
        bottle = gbt.load_bottle(name)
        bottle.parse_filename()
        if bottle.file_metadata["channel"] in ["CH0", "CH1", "CH2", "CH3"]:
            # logger.info(bottle.file_metadata["channel"])
            bottle.read_header()
            channel = bottle.file_metadata["channel"]
            timestamps = bottle.get_unix_ms_timestamps()
            data = bottle.read_data()
            bottle.file.close()
            d = {
                "channel": channel,
                "time": timestamps,
                "data": data,
            }
            bottle_df = pd.DataFrame(data=d)
            bottle_dfs.append(bottle_df)
    tiledb_buffer = pd.concat(bottle_dfs, axis=0).reset_index(drop=True)
    tiledb_buffer["data"] = tiledb_buffer["data"].astype(np.int32)
    return tiledb_buffer


def build_ancillary_buffer(gbt: GtsmBottleTar, session: str):
    logger.info(
        f"{gbt.file_metadata['filename']}: loading ancillary bottles into dataframe"
    )
    bottle_dfs = []
    for i, name in enumerate(gbt.bottle_list):
        bottle = gbt.load_bottle(name)
        bottle.parse_filename()
        if bottle.file_metadata["channel"] not in ["CH0", "CH1", "CH2", "CH3"]:
            logger.info(bottle.file_metadata["channel"])
            bottle.read_header()
            channel = bottle.file_metadata["channel"]
            timestamps = bottle.get_unix_ms_timestamps()
            data = bottle.read_data()
            bottle.file.close()
            d = {
                "channel": channel,
                "time": timestamps,
                "data": data,
            }
            bottle_df = pd.DataFrame(data=d)
            bottle_dfs.append(bottle_df)
    tiledb_buffer = pd.concat(bottle_dfs, axis=0).reset_index(drop=True)
    tiledb_buffer["data"] = tiledb_buffer["data"].astype(np.float64)
    return tiledb_buffer


def write(uri, df):
    writer = RawStrainWriter(uri)
    writer.write_df_to_tiledb(df)
    writer.array.cleanup_meta()


def bottle2tdb(network, station, filename, session):

    session_edid = get_session_edid(network, station, session)
    gbt = GtsmBottleTar(f"bottles/{filename}", session)
    # uri = f"s3://tiledb-strain/{edid}.tdb"
    strain_uri = f"arrays/{session_edid}.tdb"
    strain_buffer = build_strain_buffer(gbt, session)
    # logger.info(f"\n{strain_buffer}")
    if session.casefold() == "Day".casefold():
        station_edid = get_station_edid(network, station)
        ancillary_uri = f"arrays/{station_edid}_ancillary.tdb"
        ancillary_buffer = build_ancillary_buffer(gbt, session)
        # logger.info(f"\n{ancillary_buffer}")
    gbt.delete_bottles_from_disk()

    try:
        logger.info(f"{filename}: Writing to {strain_uri}")
        write(strain_uri, strain_buffer)
    except tiledb.TileDBError as e:
        logger.error(e)
        array = StrainArray(uri=strain_uri)
        array.create(schema_type="2D_INT", schema_source="s3")
        logger.info(f"{filename}: Writing to {strain_uri}")
        write(strain_uri, strain_buffer)

    if session.casefold() == "Day".casefold():
        try:
            logger.info(f"{filename}: Writing to {ancillary_uri}")
            write(ancillary_uri, ancillary_buffer)
        except tiledb.TileDBError as e:
            logger.error(e)
            array = StrainArray(uri=ancillary_uri)
            array.create(schema_type="2D_FLOAT", schema_source="s3")
            logger.info(f"{filename}: Writing to {ancillary_uri}")
            write(ancillary_uri, ancillary_buffer)
