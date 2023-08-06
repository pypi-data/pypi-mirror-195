from __future__ import annotations
import asyncclick as ac
import typing as t
from xoa_utils.clicks.click_commands.group import xoa_util
from xoa_utils.clicks import click_backend as cb
from xoa_utils.cmds import CmdContext
from xoa_driver.hlfuncs import anlt_ll_debug as debug_utils


@xoa_util.group(cls=cb.XenaGroup)
def debug():
    """
    Commands for debugging.\n
    """


# --------------------------
# command: init
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def init(context: ac.Context, serdes: int) -> str:
    """
    Debug: Initialize debug on the specified serdes.

        <SERDES>: The serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    inf = await debug_utils.init(port_obj, serdes)
    storage.store_anlt_low(serdes, inf)
    return str(inf)


async def _help_get(func: t.Callable, context: ac.Context, serdes: int) -> str:
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    return str(await func(port_obj, serdes, inf=inf))


async def _help_set(
    func: t.Callable, context: ac.Context, serdes: int, value: int
) -> str:
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    await func(port_obj, serdes, value=value, inf=inf)
    return ""


# --------------------------
# command: serdes-reset
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def serdes_reset(context: ac.Context, serdes: int) -> str:
    """
    Debug: Reset the specified serdes.

        <SERDES>: The serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    await debug_utils.serdes_reset(port_obj, serdes, inf=inf)
    return ""


# --------------------------
# command: mode-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def mode_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Get mode of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.mode_get, context, serdes)


# --------------------------
# command: mode-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def mode_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Set mode of the specified serdes.

        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """

    return await _help_set(debug_utils.mode_set, context, serdes, value)


# --------------------------
# command: lt-tx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_tx_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT TX configuration of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_tx_config_get, context, serdes)


# --------------------------
# command: lt-tx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_tx_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write LT TX configuration of the specified serdes.

        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """
    return await _help_set(debug_utils.lt_tx_config_set, context, serdes, value)


# --------------------------
# command: lt-rx-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX configuration of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_config_get, context, serdes)


# --------------------------
# command: lt-rx-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_config_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write LT RX configuration of the specified serdes.

        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """
    return await _help_set(debug_utils.lt_rx_config_set, context, serdes, value)


# --------------------------
# command: lt-tx-tf-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_tx_tf_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT TX Training Frames of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_tx_tf_get, context, serdes)


# --------------------------
# command: lt-tx-tf-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_tx_tf_set(context: ac.Context, serdes: int, value: int) -> str:
    """
    Debug: Write LT TX Test Frame to the specified serdes.


        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """
    return await _help_set(debug_utils.lt_tx_tf_set, context, serdes, value)


# --------------------------
# command: lt-rx-tf-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_tf_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX Test Frame of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_tf_get, context, serdes)


# --------------------------
# command: lt-rx-error-stat0-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_error_stat0_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX Error Stat0 of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_error_stat0_get, context, serdes)


# --------------------------
# command: lt-rx-error-stat1-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_error_stat1_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX Error Stat1 of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_error_stat1_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-config-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_config_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX analyzer configuration of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_analyzer_config_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-trig-mask-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_trig_mask_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX analyzer trigger mask of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_analyzer_trig_mask_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-status-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_status_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX analyzer status of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_analyzer_status_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-rd-addr-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_addr_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX analyzer RD Address of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_analyzer_rd_addr_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-rd-page-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_page_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX analyzer RD Page of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_analyzer_rd_page_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-rd-data-get
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_data_get(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read LT RX analyzer RD Data of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_rx_analyzer_rd_data_get, context, serdes)


# --------------------------
# command: lt-rx-analyzer-config-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_config_set(
    context: ac.Context, serdes: int, value: int
) -> str:
    """
    Debug: Write LT RX Analyzer configuration of the specified serdes.

        <SERDES>: The serdes index.
        VALUE INT: Specifies the value.\n
    """
    await _help_set(debug_utils.lt_rx_analyzer_config_set, context, serdes, value)
    return ""


# --------------------------
# command: lt-rx-analyzer-trig-mask-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_trig_mask_set(
    context: ac.Context, serdes: int, value: int
) -> str:
    """
    Debug: Write LT RX analyzer trigger mask of the specified serdes.

        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """
    await _help_set(debug_utils.lt_rx_analyzer_trig_mask_set, context, serdes, value)
    return ""


# --------------------------
# command: lt-rx-analyzer-rd-addr-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_addr_set(
    context: ac.Context, serdes: int, value: int
) -> str:
    """
    Debug: Write LT RX analyzer RD Address of the specified serdes.

        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """
    await _help_set(debug_utils.lt_rx_analyzer_rd_addr_set, context, serdes, value)
    return ""


# --------------------------
# command: lt-rx-analyzer-rd-page-set
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.argument("value", type=ac.INT)
@ac.pass_context
async def lt_rx_analyzer_rd_page_set(
    context: ac.Context, serdes: int, value: int
) -> str:
    """
    Debug: Write LT RX analyzer RD Page of the specified serdes.

        <SERDES>: The serdes index.

        <VALUE>: Specifies the value.
    """
    await _help_set(debug_utils.lt_rx_analyzer_rd_page_set, context, serdes, value)
    return ""


# --------------------------
# command: lt-status
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_status(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read the LT status of the specified serdes.

        <SERDES>: The serdes index.
    """
    return await _help_get(debug_utils.lt_status, context, serdes)


# --------------------------
# command: lt-prbs
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.pass_context
async def lt_prbs(context: ac.Context, serdes: int) -> str:
    """
    Debug: Read PRBS BER of the specified serdes.

        <SERDES>: The serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    return str(await debug_utils.lt_prbs(port_obj, serdes, inf=inf))


# --------------------------
# command: lt-rx-analyzer-dump
# --------------------------
@debug.command(cls=cb.XenaCommand)
@ac.argument("serdes", type=ac.INT)
@ac.option("-f", "--filename", type=ac.STRING, default="")
@ac.pass_context
async def lt_rx_analyzer_dump(context: ac.Context, serdes: int, filename: str) -> str:
    """
    Debug: Show the LT RX analyzer dump

        <SERDES>: The serdes index.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    or_inf = inf = storage.retrieve_anlt_low()
    if storage.retrieve_anlt_serdes() == serdes or or_inf is not None:
        inf = or_inf
    else:
        inf = await debug_utils.init(port_obj, serdes)
        storage.store_anlt_low(serdes, inf)
    ret_str = await debug_utils.lt_rx_analyzer_dump(port_obj, serdes, inf=inf)
    if filename:
        with open(filename, "w+") as f:
            f.write(f"{ret_str}\n")
        return "Result stored in file"
    else:
        return ret_str
