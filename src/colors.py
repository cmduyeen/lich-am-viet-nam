"""RFC 7986 uses CSS named colors; preserve requested RGB in an extension.

Clients may ignore event colors. Calendar-level Apple RGB remains unchanged.
"""
PALETTE = dict(black='000000', white='FFFFFF', red='FF0000', lime='00FF00',
 blue='0000FF', yellow='FFFF00', cyan='00FFFF', magenta='FF00FF',
 silver='C0C0C0', gray='808080', maroon='800000', olive='808000',
 green='008000', purple='800080', teal='008080', navy='000080',
 orange='FFA500', darkorange='FF8C00', tomato='FF6347', crimson='DC143C',
 dodgerblue='1E90FF', royalblue='4169E1', gold='FFD700', pink='FFC0CB',
 brown='A52A2A', indigo='4B0082', coral='FF7F50')

def rgb(value):
    return tuple(int(value[i:i+2],16) for i in (0,2,4))

def add_event_color(event, value):
    target = rgb(value.lstrip('#'))
    name = min(PALETTE, key=lambda n: sum((a-b)**2 for a,b in zip(target,rgb(PALETTE[n]))))
    event.add('color', name)
    event.add('x-lunar-color', value)
