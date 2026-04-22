from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def _handle_ConnectionUp(event):
    log.info("Switch connected - installing static rules")

    # h1 → h2
    msg = of.ofp_flow_mod()
    msg.match.in_port = 1
    msg.actions.append(of.ofp_action_output(port=2))
    event.connection.send(msg)

    # h2 → h3
   
    msg = of.ofp_flow_mod()
    msg.match.in_port = 2
    msg.actions.append(of.ofp_action_output(port=3))
    event.connection.send(msg)

    # reverse path (important!)
    msg = of.ofp_flow_mod()
    msg.match.in_port = 3
    msg.actions.append(of.ofp_action_output(port=2))
    event.connection.send(msg)

    msg = of.ofp_flow_mod()
    msg.match.in_port = 2
    msg.actions.append(of.ofp_action_output(port=1))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)