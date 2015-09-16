from structMan.model import Model

if __name__ == '__main__':
    mod = Model()
    mod.sefile = 'MappingSE2FE.txt'
    mod.safile = 'MappingSEA2SE.txt'
    mod.bdfpath = 'fus_section.bdf'
    #mod.op2path = 'model.op2'
    mod.build()
    #mod.read_op2(vectorized=True)

    panel = mod.panels['Panel.1.1']
    panel.t_lb = 0.1
    panel.t_ub = 3.3
    panel.constrain_vonMises(50.)
    panel.constrain_buckling(method=1)

    panel = mod.panels['Panel.2.1']
    panel.t_lb = 0.1
    panel.t_ub = 3.3
    panel.constrain_vonMises(50.)
    panel.constrain_buckling(method=1)


    # Z_t
    stringer = mod.stringers['Stringer.1.1']
    stringer.profile = 'Z_t'
    stringer.h = 50.
    stringer.b = 30.
    stringer.t = 1.
    stringer.t_lb = 0.5
    stringer.t_ub = 3.

    stringer.constrain_stress_tension(40.)
    stringer.constrain_stress_compression(40.)
    stringer.constrain_buckling(method=1)

    # Z_t_b
    stringer = mod.stringers['Stringer.2.1']
    stringer.profile = 'Z_t_b'
    stringer.h = 50.
    stringer.b = 30.
    stringer.b_lb = 20.
    stringer.b_ub = 50.
    stringer.t = 1.
    stringer.t_lb = 0.5
    stringer.t_ub = 3.

    stringer.constrain_stress_tension(40.)
    stringer.constrain_stress_compression(40.)
    stringer.constrain_buckling(method=1)

    # Z_t_b_h
    stringer = mod.stringers['Stringer.3.1']
    stringer.profile = 'Z_t_b_h'
    stringer.h = 50.
    stringer.h_lb = 50.
    stringer.h_ub = 70.
    stringer.b = 30.
    stringer.b_lb = 20.
    stringer.b_ub = 50.
    stringer.t = 1.
    stringer.t_lb = 0.5
    stringer.t_ub = 3.
    stringer.constrain_stress_tension(40.)
    stringer.constrain_stress_compression(40.)
    stringer.constrain_buckling(method=1)

    # Z_tf_tw_b_h
    stringer = mod.stringers['Stringer.4.1']
    stringer.profile = 'Z_tf_tw_b_h'
    stringer.h = 50.
    stringer.h_lb = 50.
    stringer.h_ub = 70.
    stringer.b = 30.
    stringer.b_lb = 20.
    stringer.b_ub = 50.
    stringer.tf = 1.
    stringer.tf_lb = 0.5
    stringer.tf_ub = 3.
    stringer.tw = 2.
    stringer.tw_lb = 0.5
    stringer.tw_ub = 5.
    stringer.constrain_stress_tension(40.)
    stringer.constrain_stress_compression(40.)
    #stringer.constrain_buckling(method=1)

    # B_t
    stringer = mod.stringers['Stringer.5.1']
    stringer.profile = 'B_t'
    stringer.h = 50.
    stringer.t = 1.
    stringer.t_lb = 0.5
    stringer.t_ub = 3.
    stringer.constrain_stress_tension(40.)
    stringer.constrain_stress_compression(40.)
    stringer.constrain_buckling(method=1)

    # B_t_h
    stringer = mod.stringers['Stringer.6.1']
    stringer.profile = 'B_t_h'
    stringer.h = 50.
    stringer.h_lb = 50.
    stringer.h_ub = 70.
    stringer.t = 1.
    stringer.t_lb = 0.5
    stringer.t_ub = 3.
    stringer.constrain_stress_tension(40.)
    stringer.constrain_stress_compression(40.)
    stringer.constrain_buckling(method=1)


    # InnerFlange t
    inner = mod.innerflanges['InnerFlange.1.1']
    inner.profile = 't'
    inner.b = 50.
    inner.t = 1.
    inner.t_lb = 0.5
    inner.t_ub = 3.
    inner.constrain_stress_tension(40.)
    inner.constrain_stress_compression(40.)
    inner.constrain_buckling(method=1)

    # InnerFlange t_b
    inner = mod.innerflanges['InnerFlange.2.1']
    inner.profile = 't_b'
    inner.t = 1.
    inner.t_lb = 0.5
    inner.t_ub = 3.
    inner.b = 50.
    inner.b_lb = 40.
    inner.b_ub = 100.
    inner.constrain_stress_tension(40.)
    inner.constrain_stress_compression(40.)
    inner.constrain_buckling(method=1)

    mod.optmodel.set_output_file('optcard.bdf')
    mod.optmodel.print_model()

