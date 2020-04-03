#helperrrrrrrrrrr
def check_assign(assign, var_list_list):
    lut = {}
    for i in range(len(assign)):
        curr_assign = assign[i]
        curr_vars = var_list_list[i]
        for j in range(len(curr_vars)):
            var = curr_vars[j]
            val = curr_assign[j]
            if var not in lut: # not in lut, add to it
                lut[var] = val
            elif lut[var] != val: # in lut, conflict val, reject
                return {}
    return lut
def multiply_factors(Factors):
    '''return a new factor that is the product of the factors in Factors'''

    #You must implement this function

    var_raw_list = list(map(Factor.get_scope, Factors))
    var_list = sum(var_raw_list, [])
    var_set = set(var_list)

    name = "Mult[" + " + ".join(f.name for f in Factors) + "]"

    var_dom_list = list(map(lambda vs: list(map(Variable.domain, vs)),
                            var_raw_list))

    if len(var_set) == len(var_list):

        poss = (product(*f) for f in var_dom_list)
        all_poss = product(*poss)
        vals = []
        for assign in all_poss:
            val = 1
            for i in range(len(Factors)):
                val *= Factors[i].get_value(list(assign[i]))
            assign_list = sum((list(a) for a in assign), [])
            vals.append(assign_list + [val])

    else: # have common var

        # remove duplicate assignments
        already_assign = set()
        # shrink factor scope to unique vars
        var_list_new = []
        for v in var_list:
            if v not in var_list_new:
                var_list_new.append(v)
        var_list = var_list_new

        poss = (product(*f) for f in var_dom_list)
        all_poss = product(*poss)
        vals = []
        for assign in all_poss:
            # var -> val assignment lut
            good_assign = check_assign(assign, var_raw_list)
            # reject conflict assignments
            if not good_assign:
                continue

            val = 1
            for i in range(len(Factors)):
                dom = Factors[i].get_scope()
                factor_assign = list(map(lambda v: good_assign[v], dom))
                val *= Factors[i].get_value(factor_assign)
            assign_list = list(map(lambda v: good_assign[v], var_list))

            if tuple(assign_list) not in already_assign:
                already_assign.add(tuple(assign_list))
                vals.append(assign_list + [val])

    f = Factor(name, var_list)
    f.add_values(vals)
    return f





from itertools import product


def restrict_factor(f, var, value):
    '''f is a factor, var is a Variable, and value is a value from var.domain.
    Return a new factor that is the restriction of f by this var = value.
    Don't change f! If f has only one variable its restriction yields a
    constant factor'''
    #IMPLEMENT
    var_list = f.get_scope()
    idx = var_list.index(var)
    var_list_new = [v for v in var_list if v != var]
    ff = Factor(f.name + "[R:" + var.name + "]", var_list_new)

    # restrict var domain to be {value}
    domain = list(map(Variable.domain, var_list))
    domain[idx] = [value]
    vals = []
    for assign in product(*domain):
        val = f.get_value(list(assign))
        assign_list = list(assign)
        # generate assign, ignore var = value, since it's fixed
        assign_list.pop(idx)
        vals.append(assign_list + [val])

    ff.add_values(vals)
    return ff



def sum_out_variable(f, var):
    '''return a new factor that is the product of the factors in Factors
       followed by the suming out of Var'''
    #IMPLEMENT
    var_list = f.get_scope()
    idx = var_list.index(var)
    var_list_new = [v for v in var_list if v != var]
    ff = Factor(f.name + "[S:" + var.name + "]", var_list_new)

    # consider product of other var dom
    domain_new = list(map(Variable.domain, var_list_new))
    vals = []
    for assign in product(*domain_new):
        val = 0
        for v in var.domain():
            assign_list = list(assign)
            # insert var = v into assignment
            assign_list.insert(idx, v)
            val += f.get_value(assign_list)
        vals.append(list(assign) + [val])

    ff.add_values(vals)
    return ff
    


###
def VE(Net, QueryVar, EvidenceVars):
    '''
    Input: Net---a BN object (a Bayes Net)
           QueryVar---a Variable object (the variable whose distribution
                      we want to compute)
           EvidenceVars---a LIST of Variable objects. Each of these
                          variables has had its evidence set to a particular
                          value from its domain using set_evidence. 

   VE returns a distribution over the values of QueryVar, i.e., a list
   of numbers one for every value in QueryVar's domain. These numbers
   sum to one, and the i'th number is the probability that QueryVar is
   equal to its i'th value given the setting of the evidence
   variables. For example if QueryVar = A with Dom[A] = ['a', 'b',
   'c'], EvidenceVars = [B, C], and we have previously called
   B.set_evidence(1) and C.set_evidence('c'), then VE would return a
   list of three numbers. E.g. [0.5, 0.24, 0.26]. These numbers would
   mean that Pr(A='a'|B=1, C='c') = 0.5 Pr(A='a'|B=1, C='c') = 0.24
   Pr(A='a'|B=1, C='c') = 0.26
    '''
    #IMPLEMENT

    F = Net.factors()
    E = EvidenceVars
    Q = QueryVar

    FF = []
    Eset = set(E)
    for f in F:
        restrict_vars = Eset.intersection(f.get_scope())
        if len(restrict_vars) > 0: # f can be restricted
            ff = f
            for ef in restrict_vars:
                ff = restrict_factor(ff, ef, ef.get_evidence())
            FF.append(ff)
        else:
            FF.append(f)

    Z = min_fill_ordering(FF, Q)
    for z in Z:
        fs = [ff for ff in FF if z in ff.get_scope()]
        g = sum_out_variable(multiply_factors(fs), z)
        FF = [ff for ff in FF if ff not in fs]
        FF.append(g)

    f = multiply_factors(FF)

    # perform normalization to generate prob
    # use inf to deal with division by zero
    dist = [f.get_value([v]) for v in Q.domain()]
    total = sum(dist)
    if total == 0:
        return [float('inf') for val in dist]
    else:
        return [val / total for val in dist]


