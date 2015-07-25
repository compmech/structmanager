"""
Optimization cards (:mod:`feopt.genesis.cards_solver`)
================================================

.. currentmodule:: feopt.genesis.cards_solver`

Many input cards related to the finite element solver are wrapped in this
module.

"""
from genesis import Genesis


class PBARL(Genesis):
    """Pre-defined sections for bar elements

    ============  ============================================================
    Attribute     Description
    ============  ============================================================
    ``id``        ``int`` - property id
    ``mid``       ``int`` - material id
    ``library``   ``str`` - the default library used to calculate the section
                  properties (``'CSLIB1'``, etc)
    ``d_list``    ``list`` - design variables
    ``type``      ``str`` - section type (``'RECT'``, etc)
    ``nsm``       ``float`` - non-structural mass in [mass unit]/[metric unit]
    ============  ============================================================

    """
    def __init__(self, id, mid, library, type, d_list, nsm=0.):
        Genesis.__init__(self)
        self.id = int(id)
        self.mid = int(mid)
        self.library = library.strip()
        self.type = type.strip()
        self.d_list = d_list
        self.nsm = nsm
        #
        #if self.library == 'CSLIB1':
        #   axis_v = 'Z'
        #    axis_h = 'Y'
        #elif self.library == 'CSLIB2':
        #    axis_v = 'Y'
        #    axis_h = 'Z'
        #

    def print_card(self, file):
        """Prints the corresponding input card

        Parameters
        ----------
        file : file
            File object with a :meth:`write` method.

        """
        pbarlstr = ('%s,%d,%d,%s,%s' % ('PBARL', self.id, self.mid,\
                    self.library, self.type))
        file.write (pbarlstr + '\n')
        pbarlstr = '+'
        for d in self.d_list:
            pbarlstr = pbarlstr + ',' + str(float(d))
        pbarlstr = pbarlstr + ',' + str(self.nsm)
        file.write (pbarlstr + '\n')

