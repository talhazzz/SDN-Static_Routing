from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def _handle_ConnectionUp(event):
    log.info("Installing WRONG rules")

    # WRONG: send both to same port
    msg = of.ofp_flow_mod()
    msg.match.in_port = 1
    msg.actions.append(of.ofp_action_output(port=1))  # wrong
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.match.in_port = 2
    msg.actions.append(of.ofp_action_output(port=2))  # wrong
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)