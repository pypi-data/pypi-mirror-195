from __future__ import annotations
import asyncclick as ac
import json
import typing as t
from xoa_driver.hlfuncs import anlt as anlt_utils
from xoa_utils.clicks import click_backend as cb
from xoa_utils.clis import format_recovery, format_port_status
from xoa_utils.clicks.click_commands.group import xoa_util
from xoa_utils.clicks import click_help as h
from xoa_utils.cmds import CmdContext
from enum import Enum


class ASCIIStyle(Enum):
    DARKRED = "\033[31m"
    DARKGREEN = "\033[32m"
    DARKYELLOW = "\033[33m"
    DARKBLUE = "\033[34m"
    DARKMAGENTA = "\033[35m"
    DARKCYAN = "\033[36m"

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"

    DARKRED_BG = "\033[41m"
    DARKGREEN_BG = "\033[42m"
    DARKYELLOW_BG = "\033[43m"
    DARKBLUE_BG = "\033[44m"
    DARKMAGENTA_BG = "\033[45m"
    DARKCYAN_BG = "\033[46m"

    RED_BG = "\033[101m"
    GREEN_BG = "\033[102m"
    YELLOW_BG = "\033[103m"
    BLUE_BG = "\033[104m"
    MAGENTA_BG = "\033[105m"
    CYAN_BG = "\033[106m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


@xoa_util.group(cls=cb.XenaGroup)
def anlt():
    """
    Commands for AN/LT.
    """


# --------------------------
# command: recovery
# --------------------------
@anlt.command(cls=cb.XenaCommand)
@ac.option("--on/--off", type=ac.BOOL, help=h.HELP_RECOVERY_ON, default=True)
@ac.pass_context
async def recovery(context: ac.Context, on: bool) -> str:
    """
    Enable/disable link recovery on the working port.
    If enable, the port will keep doing AN/LT when no link-up signal is detected.
    """
    storage: CmdContext = context.obj

    port_obj = storage.retrieve_port()
    await anlt_utils.anlt_link_recovery(port_obj, on)
    return format_recovery(storage, on)


# --------------------------
# command: status
# --------------------------
@anlt.command(cls=cb.XenaCommand)
@ac.pass_context
async def status(context: ac.Context) -> str:
    """
    Show AN/LT status of the working port.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    status_dic = await anlt_utils.anlt_status(port_obj)
    port_id = storage.retrieve_port_str()
    return format_port_status(port_id, status_dic, storage)


# --------------------------
# command: do
# --------------------------
@anlt.command(cls=cb.XenaCommand)
@ac.pass_context
async def do(context: ac.Context) -> str:
    """
    Apply and start AN/LT to the working port.
    """
    storage: CmdContext = context.obj
    port_obj = storage.retrieve_port()
    an_enable = storage.retrieve_an_enable()
    lt_enable = storage.retrieve_lt_enable()
    an_allow_loopback = storage.retrieve_an_loopback()
    lt_preset0 = storage.retrieve_lt_preset0()
    lt_initial_modulations = storage.retrieve_lt_initial_mod()
    lt_interactive = storage.retrieve_lt_interactive()
    lt_algorithm = storage.retrieve_lt_algorithm()
    await anlt_utils.anlt_start(
        port_obj,
        an_enable,
        lt_enable,
        an_allow_loopback,
        lt_preset0,
        lt_initial_modulations,
        lt_interactive,
        lt_algorithm,
    )
    return ""


# **************************
# command: log
# **************************
@anlt.command(cls=cb.XenaCommand, name="log")
@ac.option(
    "-f", "--filename", type=ac.STRING, help=h.HELP_ANLT_LOG_FILENAME, default=""
)
@ac.option(
    "-k",
    "--keep",
    type=ac.Choice(["all", "an", "lt"]),
    help=h.HELP_ANLT_LOG_KEEP,
    default="all",
)
@ac.option("-s", "--serdes", type=ac.STRING, help=h.HELP_ANLT_LOG_SERDES, default="")
@ac.pass_context
async def anlt_log(ctx: ac.Context, filename: str, keep: str, serdes: str) -> str:
    """
    Start AN/LT logging.
    """

    def _filter_log(log: str, keep: str, serdes: list[int]) -> list[dict]:
        all_logs = []
        for lg in log.split("\n"):
            try:
                content = json.loads(lg)
                log_serdes = content["lane"]
                module = content["module"]

                serdes_in = (serdes and log_serdes in serdes) or (not serdes)
                keep_in = any(
                    (
                        keep == "an" and "AN" in module,
                        keep == "lt" and "LT" in module,
                        keep == "all",
                    )
                )
                if serdes_in and keep_in:
                    all_logs.append(content)

            except Exception:
                pass
        return all_logs

    def _dict_get(dic: dict, *keys: str) -> t.Any:
        current = dic
        for k in keys:
            current = current.get(k, "")
            if current == "":
                break
        return current

    def _flatten(dic: dict[str, str]) -> str:
        return "".join((f"{k}: {v:<7}" for k, v in dic.items()))

    def _ascii_styler(str: str, fg_style: list[ASCIIStyle]) -> str:
        style = "".join(s.value for s in fg_style)
        return f"{style}{str}{ASCIIStyle.END.value}"

    def _beautify(filtered: list[dict]) -> str:
        real = []
        for i in filtered:
            b_str = ""

            log_time = _dict_get(i, "time")
            log_entry = _dict_get(i, "entry")
            log_type = _dict_get(i, "type")
            log_m = _dict_get(i, "module")
            log_log = _dict_get(i, "entry", "log")
            log_serdes = _dict_get(i, "lane")
            log_m = _dict_get(i, "module")
            log_m = _dict_get(i, "module")
            log_event = _dict_get(i, "entry", "fsm", "event")
            log_current = _dict_get(i, "entry", "fsm", "current")
            log_new = _dict_get(i, "entry", "fsm", "new")
            log_direction = _dict_get(i, "entry", "direction")
            if log_direction == "tx":
                log_direction = _ascii_styler(
                    log_direction.upper(), [ASCIIStyle.DARKBLUE_BG]
                )
            else:
                log_direction = _ascii_styler(
                    log_direction.upper(), [ASCIIStyle.DARKGREEN_BG]
                )

            log_value = _dict_get(i, "entry", "pkt", "value")
            log_ptype = _dict_get(i, "entry", "pkt", "type")
            log_pstate = _dict_get(i, "entry", "pkt", "state")
            log_np = _dict_get(i, "entry", "pkt", "fields", "NP")
            log_ack = _dict_get(i, "entry", "pkt", "fields", "Ack")
            log_rf = _dict_get(i, "entry", "pkt", "fields", "RF")
            log_tn = _dict_get(i, "entry", "pkt", "fields", "TN")
            log_en = _dict_get(i, "entry", "pkt", "fields", "EN")
            log_c = _dict_get(i, "entry", "pkt", "fields", "C")
            log_fec = _dict_get(i, "entry", "pkt", "fields", "fec")
            log_ab = _dict_get(i, "entry", "pkt", "fields", "ability")
            log_pkt_ctrl = _dict_get(i, "entry", "pkt", "fields", "control")
            log_pkt_status = _dict_get(i, "entry", "pkt", "fields", "status")
            log_pkt_locked = _dict_get(i, "entry", "pkt", "fields", "locked")
            log_mp = _dict_get(i, "entry", "pkt", "fields", "MP")
            log_ack2 = _dict_get(i, "entry", "pkt", "fields", "Ack2")
            log_t = _dict_get(i, "entry", "pkt", "fields", "T")
            log_fmt_v = _dict_get(
                i, "entry", "pkt", "fields", "formatted message", "value"
            )
            log_fmt_msg = _dict_get(
                i, "entry", "pkt", "fields", "formatted message", "message"
            )
            log_ufmt_v = _dict_get(
                i, "entry", "pkt", "fields", "un-formatted message", "value"
            )
            log_ufmt_msg = _dict_get(
                i, "entry", "pkt", "fields", "un-formatted message", "message"
            )
            log_ufmt_fec = _dict_get(
                i, "entry", "pkt", "fields", "un-formatted message", "fec"
            )
            log_ufmt_ab = _dict_get(
                i, "entry", "pkt", "fields", "un-formatted message", "ability"
            )

            if log_pkt_locked == "true":
                log_pkt_locked = _ascii_styler(log_pkt_locked, [ASCIIStyle.GREEN_BG])
            else:
                log_pkt_locked = _ascii_styler(log_pkt_locked, [ASCIIStyle.RED_BG])

            log_pkt_done = _dict_get(i, "entry", "pkt", "fields", "done")
            if log_pkt_done == "true":
                log_pkt_done = _ascii_styler(log_pkt_done, [ASCIIStyle.GREEN_BG])
            else:
                log_pkt_done = _ascii_styler(log_pkt_done, [ASCIIStyle.RED_BG])

            log_pkt_value = _dict_get(i, "entry", "pkt", "value")

            serdes_str = f"(S{log_serdes})," if "LT" in log_m else ","
            common = f"{log_time/1000000}, {log_m}{serdes_str}"

            if log_type == "debug":
                b_str = f"{common:<32}{'DBG:':<5}{log_log}"
            elif log_type == "fsm":
                b_str = (
                    f"{common:<32}{'FSM:':<5}({log_event}) {log_current} -> {log_new}"
                )
            elif log_type == "trace" and "log" in log_entry:
                b_str = f"{common:<32}{'MSG:':<5}{log_log}"
            elif log_type == "trace" and "direction" in log_entry and "LT" not in log_m:
                if log_pstate == "new" or log_pstate == "":
                    if log_ptype == "base page":
                        b_str = f"{common:<32}{(log_direction + ':'):<14}{log_value}, {log_ptype}, NP:{int(log_np, 0)}, ACK:{int(log_ack, 0)}, RF:{int(log_rf, 0)}, TN:{int(log_tn, 0)}, EN:{int(log_en ,0)}, C:{int(log_c, 0)}\n{'':<37}FEC:{log_fec}, ABILITY:{log_ab}"
                    else:
                        if log_fmt_v:
                            b_str = f"{common:<32}{(log_direction + ':'):<14}{log_value}, {log_ptype}, NP:{int(log_np, 0)}, ACK:{int(log_ack, 0)}, MP:{int(log_mp, 0)}, ACK2:{int(log_ack2, 0)}, T:{int(log_t ,0)}\n{'':<37}Formatted message:\n{'':<37}Value:{log_fmt_v}, Msg:{log_fmt_msg}"
                        else:
                            b_str = f"{common:<32}{(log_direction + ':'):<14}{log_value}, {log_ptype}, NP:{int(log_np, 0)}, ACK:{int(log_ack, 0)}, MP:{int(log_mp, 0)}, ACK2:{int(log_ack2, 0)}, T:{int(log_t ,0)}\n{'':<37}Un-formatted message:\n{'':<37}Value:{log_ufmt_v}, Msg:{log_ufmt_msg}\n{'':<37}FEC:{log_ufmt_fec}, ABILITY:{log_ufmt_ab}"
            elif log_type == "trace" and "direction" in log_entry and "LT" in log_m:
                if log_pstate == "new" or log_pstate == "":
                    b_str = f"{common:<32}{(log_direction + ':'):<14}{log_pkt_value}, LOCKED={log_pkt_locked}, DONE={log_pkt_done}\n{'':<37}{_flatten(log_pkt_ctrl)}\n{'':<37}{_flatten(log_pkt_status)}"

            if b_str:
                real.append(b_str)
        return "\n".join(real)

    async def log(
        storage: CmdContext, filename: str, keep: str, serdes: list[int]
    ) -> str:
        port_obj = storage.retrieve_port()
        log_str = await anlt_utils.anlt_log(port_obj)
        filtered = _filter_log(log_str, keep, serdes)
        string = _beautify(filtered)
        if filename and log_str:
            with open(filename, "a") as f:
                f.write(f"{log_str}\n")
        return string

    real_serdes_list = [int(i.strip()) for i in serdes.split(",")] if serdes else []
    kw = {"filename": filename, "keep": keep, "serdes": real_serdes_list}
    storage: CmdContext = ctx.obj
    storage.set_loop_coro(log, kw)
    return ""
