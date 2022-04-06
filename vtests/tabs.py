from neoscore.common import *

neoscore.setup()

flowable = Flowable(ORIGIN, None, Mm(500), Mm(40))

# 6 line tab

staff_1 = TabStaff(ORIGIN, flowable, Mm(500))
clef_1 = TabClef(ZERO, staff_1)

TabNumber(Mm(5), staff_1, 1, 1)
TabNumber(Mm(7), staff_1, 1, 2)
TabNumber(Mm(7), staff_1, 2, 1)
TabNumber(Mm(7), staff_1, 3, 1)
TabNumber(Mm(7), staff_1, 4, 2)
TabNumber(Mm(7), staff_1, 5, 3)
TabNumber(Mm(7), staff_1, 6, 0)
TabNumber(Mm(10), staff_1, 1, 9)
TabNumber(Mm(13), staff_1, 4, 123)

# Rolled chord

chord_notes = [
    TabNumber(Mm(22), staff_1, 1, 2),
    TabNumber(Mm(22), staff_1, 2, 1),
    TabNumber(Mm(22), staff_1, 3, 1),
    TabNumber(Mm(22), staff_1, 4, 2),
    TabNumber(Mm(22), staff_1, 5, 3),
]
u = staff_1.unit
arp = ArpeggioLine((u(-1), u(-1)), chord_notes[0], (u(-1), u(2)), chord_notes[-1], True)


# 4 line tab

staff_2 = TabStaff((ZERO, Mm(15)), flowable, Mm(500), line_count=4)
clef_2 = TabClef(ZERO, staff_2, "4stringTabClef")


regular_staff = Staff((ZERO, Mm(30)), flowable, Mm(500))
Clef(ZERO, regular_staff, "treble")

all_staves = [staff_1, staff_2, regular_staff]

Barline(Mm(20), all_staves)

neoscore.show()