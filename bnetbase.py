'''Classes for variable elimination Routines 
   A) class BN_Variable

      This class allows one to define Bayes Net variables.

      On initialization the variable object can be given a name and a
      domain of values. This list of domain values can be added to or
      deleted from in support of an incremental specification of the
      variable domain.

      The variable also has a set and get value method. These set a
      value for the variable that can be used by the factor class. 


    B) class factor

      This class allows one to define a factor specified by a table
      of values. 

      On initialization the variables the factor is over is
      specified. This must be a list of variables. This list of
      variables cannot be changed once the constraint object is
      created.

      Once created the factor can be incrementally initialized with a
      list of values. To interact with the factor object one first
      sets the value of each variable in its scope (using the
      variable's set_value method), then one can set or get the value
      of the factor (a number) on those fixed values of the variables
      in its scope.

      Initially, one creates a factor object for every conditional
      probability table in the bayes-net. Then one initializes the
      factor by iteratively setting the values of all of the factor's
      variables and then adding the factor's numeric value using the
      add_value method. 

    C) class BN
       This class allows one to put factors and variables together to form a Bayes net.
       It serves as a convient place to store all of the factors and variables associated
       with a Bayes Net in one place. It also has some utility routines to, e.g,., find
       all of the factors a variable is involved in. 

    '''

class Variable:
    '''Class for defining Bayes Net variables. '''
    
    def __init__(self, name, domain=[]):
        '''Create a variable object, specifying its name (a
        string). Optionally specify the initial domain.
        '''
        self.name = name                #text name for variable
        self.dom = list(domain)         #Make a copy of passed domain
        self.evidence_index = 0         #evidence value (stored as index into self.dom)
        self.assignment_index = 0       #For use by factors. We can assign variables values
                                        #and these assigned values can be used by factors
                                        #to index into their tables.

    def add_domain_values(self, values):
        '''Add domain values to the domain. values should be a list.'''
        for val in values: self.dom.append(val)

    def value_index(self, value):
        '''Domain values need not be numbers, so return the index
           in the domain list of a variable value'''
        return self.dom.index(value)

    def domain_size(self):
        '''Return the size of the domain'''
        return(len(self.dom))

    def domain(self):
        '''return the variable domain'''
        return(list(self.dom))

    def set_evidence(self,val):
        '''set this variable's value when it operates as evidence'''
        self.evidence_index = self.value_index(val)

    def get_evidence(self):
        return(self.dom[self.evidence_index])

    def set_assignment(self, val):
        '''Set this variable's assignment value for factor lookups'''
        self.assignment_index = self.value_index(val)

    def get_assignment(self):
        return(self.dom[self.assignment_index])

    ##These routines are special low-level routines used directly by the
    ##factor objects
    def set_assignment_index(self, index):
        '''This routine is used by the factor objects'''
        self.assignment_index = index

    def get_assignment_index(self):
        '''This routine is used by the factor objects'''
        return(self.assignment_index)

    def __repr__(self):
        '''string to return when evaluating the object'''
        return("{}".format(self.name))
    
    def __str__(self):
        '''more elaborate string for printing'''
        return("{}, Dom = {}".format(self.name, self.dom))


class Factor: 

    '''Class for defining factors. A factor is a function that is over
    an ORDERED sequence of variables called its scope. It maps every
    assignment of values to these variables to a number. In a Bayes
    Net every CPT is represented as a factor. Pr(A|B,C) for example
    will be represented by a factor over the variables (A,B,C). If we
    assign A = a, B = b, and C = c, then the factor will map this
    assignment, A=a, B=b, C=c, to a number that is equal to Pr(A=a|
    B=b, C=c). During variable elimination new factors will be
    generated. However, the factors computed during variable
    elimination do not necessarily correspond to conditional
    probabilities. Nevertheless, they still map assignments of values
    to the variables in their scope to numbers.

    Note that if the factor's scope is empty it is a constant factor
    that stores only one value. add_values would be passed something
    like [[0.25]] to set the factor's single value. The get_value
    functions will still work.  E.g., get_value([]) will return the
    factor's single value. Constant factors might be created when a
    factor is restricted.'''

    def __init__(self, name, scope):
        '''create a Factor object, specify the Factor name (a string)
        and its scope (an ORDERED list of variable objects).'''
        self.scope = list(scope)
        self.name = name
        size = 1
        for v in scope:
            size = size * v.domain_size()
        self.values = [0]*size  #initialize values to be long list of zeros.

    def get_scope(self):
        '''returns copy of scope...you can modify this copy without affecting 
           the factor object'''
        return list(self.scope)

    def add_values(self, values):
        '''This routine can be used to initialize the factor. We pass
        it a list of lists. Each sublist is a ORDERED sequence of
        values, one for each variable in self.scope followed by a
        number that is the factor's value when its variables are
        assigned these values. For example, if self.scope = [A, B, C],
        and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], then we could pass add_values the
        following list of lists
        [[1, 'a', 'heavy', 0.25], [1, 'a', 'light', 1.90],
         [1, 'b', 'heavy', 0.50], [1, 'b', 'light', 0.80],
         [2, 'a', 'heavy', 0.75], [2, 'a', 'light', 0.45],
         [2, 'b', 'heavy', 0.99], [2, 'b', 'light', 2.25],
         [3, 'a', 'heavy', 0.90], [3, 'a', 'light', 0.111],
         [3, 'b', 'heavy', 0.01], [3, 'b', 'light', 0.1]]

         This list initializes the factor so that, e.g., its value on
         (A=2,B=b,C='light) is 2.25'''

        for t in values:
            index = 0
            for v in self.scope:
                index = index * v.domain_size() + v.value_index(t[0])
                t = t[1:]
            self.values[index] = t[0]
         
    def add_value_at_current_assignment(self, number): 

        '''This function allows adding values to the factor in a way
        that will often be more convenient. We pass it only a single
        number. It then looks at the assigned values of the variables
        in its scope and initializes the factor to have value equal to
        number on the current assignment of its variables. Hence, to
        use this function one first must set the current values of the
        variables in its scope.

        For example, if self.scope = [A, B, C],
        and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], and we first set an assignment for A, B
        and C:
        A.set_assignment(1)
        B.set_assignment('a')
        C.set_assignment('heavy')
        then we call 
        add_value_at_current_assignment(0.33)
         with the value 0.33, we would have initialized this factor to have
        the value 0.33 on the assigments (A=1, B='1', C='heavy')
        This has the same effect as the call
        add_values([1, 'a', 'heavy', 0.33])

        One advantage of the current_assignment interface to factor values is that
        we don't have to worry about the order of the variables in the factor's
        scope. add_values on the other hand has to be given tuples of values where 
        the values must be given in the same order as the variables in the factor's 
        scope. 

        See recursive_print_values called by print_table to see an example of 
        where the current_assignment interface to the factor values comes in handy.
        '''

        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        self.values[index] = number

    def get_value(self, variable_values):

        '''This function is used to retrieve a value from the
        factor. We pass it an ordered list of values, one for every
        variable in self.scope. It then returns the factor's value on
        that set of assignments.  For example, if self.scope = [A, B,
        C], and A.domain() = [1,2,3], B.domain() = ['a', 'b'], and
        C.domain() = ['heavy', 'light'], and we invoke this function
        on the list [1, 'b', 'heavy'] we would get a return value
        equal to the value of this factor on the assignment (A=1,
        B='b', C='heavy')'''

        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.value_index(variable_values[0])
            variable_values = variable_values[1:]
        return self.values[index]

    def get_value_at_current_assignments(self):

        '''This function is used to retrieve a value from the
        factor. The value retrieved is the value of the factor when
        evaluated at the current assignment to the variables in its
        scope.

        For example, if self.scope = [A, B, C], and A.domain() =
        [1,2,3], B.domain() = ['a', 'b'], and C.domain() = ['heavy',
        'light'], and we had previously invoked A.set_assignment(1),
        B.set_assignment('a') and C.set_assignment('heavy'), then this
        function would return the value of the factor on the
        assigments (A=1, B='1', C='heavy')'''
        
        index = 0
        for v in self.scope:
            index = index * v.domain_size() + v.get_assignment_index()
        return self.values[index]

    def print_table(self):
        '''print the factor's table'''
        saved_values = []  #save and then restore the variable assigned values.
        for v in self.scope:
            saved_values.append(v.get_assignment_index())

        self.recursive_print_values(self.scope)

        for v in self.scope:
            v.set_assignment_index(saved_values[0])
            saved_values = saved_values[1:]
        
    def recursive_print_values(self, vars):
        if len(vars) == 0:
            print("[",end=""),
            for v in self.scope:
                print("{} = {},".format(v.name, v.get_assignment()), end="")
            print("] = {}".format(self.get_value_at_current_assignments()))
        else:
            for val in vars[0].domain():
                vars[0].set_assignment(val)
                self.recursive_print_values(vars[1:])

    def __repr__(self):
        return("{}".format(self.name))

class BN:

    '''Class for defining a Bayes Net.
       This class is simple, it just is a wrapper for a list of factors. And it also
       keeps track of all variables in the scopes of these factors'''

    def __init__(self, name, Vars, Factors):
        self.name = name
        self.Variables = list(Vars)
        self.Factors = list(Factors)
        for f in self.Factors:
            for v in f.get_scope():     
                if not v in self.Variables:
                    print("Bayes net initialization error")
                    print("Factor scope {} has variable {} that", end='')
                    print(" does not appear in list of variables {}.".format(list(map(lambda x: x.name, f.get_scope())), v.name, list(map(lambda x: x.name, Vars))))

    def factors(self):
        return list(self.Factors)

    def variables(self):
        return list(self.Variables)

#
def multiply_factors(Factors):
    '''return a new factor that is the product of the factors in Factors'''
     #IMPLEMENT
    length_Factors = len(Factors)
#    print(type(Factors))
    factors_lst = []
    for factor in Factors:
        factors_lst.append(factor.get_scope())
    
    all_vars_lst = [] #all variables of Factors (include duplicates)
    for factor in factors_lst:
        for var in factor:
            all_vars_lst.append(var)

    unique_vars_lst = [] #all unique vars of Factors
    for factor in factors_lst:
        for var in factor:
            if var not in unique_vars_lst:
                unique_vars_lst.append(var)
    
    name = "__Multiply__{"
    for factor in Factors:
        name+=factor.name
    name+="} "

    vars_domain_lst = [] #list of each var's domain    
    for factor in factors_lst:
        dom = []
        for var in factor:
            dom.append(var.domain())
        vars_domain_lst.append(dom)
#        
    if len(unique_vars_lst) == len(all_vars_lst):
        
        var_comb_lst = []
        for var in vars_domain_lst:
            prod = product(*var)
            var_comb_lst.append(prod)
        all_var_comb_lst = product(*var_comb_lst) 
        all_var_comb_lst = list(all_var_comb_lst) #listified
        
#        print(all_var_comb_lst)
        all_var_comb_lst_listified = listify_domain(all_var_comb_lst)
#        print(list(all_var_comb_lst))
#        i.e., [(('i', 'b'),), (('i', '-b'),), (('-i', 'b'),), (('-i', '-b'),)]
        
        vars_domain_lst_ = vars_domain_lst[:]
        all_product_lst  = []
        for var in vars_domain_lst_:
            product_lst = list(product(*var))
            all_product_lst.extend(product_lst)
            

        
        if length_Factors == 1: #special case
            all_product_lst_ = all_product_lst[:] #make copy first
            factor_value_lst = []
            for comb in all_product_lst_:
                lst_comb = list(comb)
                for factor in Factors:
                    if lst_comb != []:
                        value = factor.get_value(lst_comb)
                        lst_comb.append(value)
                factor_value_lst.append(lst_comb)
        else:
            factor_value_lst = []
            all_var_comb_lst_listified = listify_domain(all_var_comb_lst)
#            print(all_var_comb_lst)
#            print(all_var_comb_lst_listified)
            for comb in all_var_comb_lst_listified:
                value = 1 #init value to 1 for multiplication
#                print(type(comb)) tuple ()
#                print(comb)
                for i in range(length_Factors):
                    combo_var = comb[i]
                    value *= Factors[i].get_value(combo_var)
                    
                final_factor_lst = []
                for val in comb:
                    val_lst = list(val)
                    final_factor_lst.extend(val_lst) #make into one list, [g] or [-g]
                    
                final_factor_value = final_factor_lst + [value]
                factor_value_lst.append(final_factor_value)
                
        
    else: # Factors have onre or more shared variables!
        explored_lst = [] #init
        all_vars_lst = unique_vars_lst #use unique vars list defined before
        var_comb_lst = []  #init
        for var in vars_domain_lst:
            prod = product(*var)
            var_comb_lst.append(prod)
            
        all_var_comb_lst = product(*var_comb_lst) 
        all_var_comb_lst = list(all_var_comb_lst) #listified
        all_var_comb_lst_listified = listify_domain(all_var_comb_lst)

        factor_value_lst = []
        for comb_lst in all_var_comb_lst_listified:
            
            valid = True
            explored_dict = {}
            for i in range(length_Factors):
                length_curr_factor = len(factors_lst[i])
#                print(length_curr_factor)
                for j in range(length_curr_factor):
#                    print(factors_lst[j])
                    if factors_lst[i][j] not in explored_dict: #init key 
                        explored_dict[factors_lst[i][j]] = comb_lst[i][j]
                    elif explored_dict[factors_lst[i][j]] != comb_lst[i][j]:
                        valid = False #find invalid/conflicting combination

            if valid is False: #invalid combination of factor and value
                continue #go to next iter of loop
        
            value = 1 #init value for mult
            for i in range(length_Factors):
                curr_factor = Factors[i]
                curr_domain = curr_factor.get_scope()
                factor_lst = []
                
                for domain in curr_domain:
#                    print(domain)
                    factor_lst.append(explored_dict[domain])
                value *= curr_factor.get_value(factor_lst)
                
            comb_list = []
            for var in all_vars_lst:
                comb_list.append(explored_dict[var])
            
            if comb_list not in explored_lst:
                explored_lst.append(comb_list)
                final_factor_value = comb_list + [value]
                factor_value_lst.append(final_factor_value)

    new_factor = Factor(name, all_vars_lst)
    new_factor.add_values(factor_value_lst)
    return new_factor




from itertools import product


def helper_get_scope_name(f, var):
    all_vars_list = f.get_scope() #list of all vars in factor f
    
    vars_list_without_var = []
    for var_ in all_vars_list:
        if var_ != var:
            vars_list_without_var.append(var_)
    
    return all_vars_list, vars_list_without_var
    

def restrict_factor(f, var, value):
    '''f is a factor, var is a Variable, and value is a value from var.domain.
    Return a new factor that is the restriction of f by this var = value.
    Don't change f! If f has only one variable its restriction yields a
    constant factor'''
    #IMPLEMENT
    
    all_vars_list, scope = helper_get_scope_name(f, var)
    
    curr_index_var = all_vars_list.index(var)
    name = f.name + "__Restrict__{"+ var.name + "}"
    new_factor = Factor(name, scope)

    domain_lst = []
    for var_ in all_vars_list:
        new_var_domain = var_.domain()
        domain_lst.append(new_var_domain)
    
#    print("d list")
#    print(domain_lst)
    
    domain_lst[curr_index_var] = [value]
    
    add_values_lst = []
    all_dom_product_lst = list(product(*domain_lst))
    all_dom_product_lst_listified = listify_domain(all_dom_product_lst)
    
    for prod in all_dom_product_lst_listified:
#        print(type(prod))
        prod_copy = prod[:] #make a copy of original prod list in f
        value = f.get_value(prod_copy)
        prod_copy.pop(curr_index_var)
        final_lst = prod_copy + [value] #i.e., ['c', 0.5]
        add_values_lst.append(final_lst)

    new_factor.add_values(add_values_lst)
    return new_factor


def listify_domain(dom_list): #return a list of lists of domain, rather than iter 
    listified_dom_list = []
    for d in dom_list:
        listified_dom_list.append(list(d))
    return listified_dom_list


def sum_out_variable(f, var):
    '''return a new factor that is the product of the factors in Factors
       followed by the suming out of Var'''
    #IMPLEMENT
    
    all_vars_list, scope = helper_get_scope_name(f, var)
    curr_index_var = all_vars_list.index(var)
    name = f.name + "__Sum_out__{"+ var.name + "}"
    
    new_factor = Factor(name, scope)
    
    domain_lst = []
    for var_ in scope:
        new_var_domain = var_.domain()
        domain_lst.append(new_var_domain)
#    print(var.domain())
##    print("end")
#    
    add_values_lst = []
    all_dom_product_lst = list(product(*domain_lst))
    all_dom_product_lst_listified = listify_domain(all_dom_product_lst)
    all_var_domain = var.domain()
    
#    print(curr_index_var)
    
    for prod in all_dom_product_lst_listified:
        value = 0
        for var_val in all_var_domain:
            prod_copy = prod[:] #make a copy of current prod list
#            assign_list = list(prod)
#            print('original lst')
            prod_copy.insert(curr_index_var, var_val)
            value += f.get_value(prod_copy)
        final_lst = prod + [value] #['c', 0.5]
        add_values_lst.append(final_lst)
        
    new_factor.add_values(add_values_lst)
    return new_factor
    
def normalize(nums):
    '''take as input a list of number and return a new list of numbers where
    now the numbers sum to 1, i.e., normalize the input numbers'''
    s = sum(nums)
    if s == 0:
        newnums = [0]*len(nums)
    else:
        newnums = []
        for n in nums:
            newnums.append(n/s)
    return newnums

###Orderings
def min_fill_ordering(Factors, QueryVar):
    '''Compute a min fill ordering given a list of factors. Return a list
    of variables from the scopes of the factors in Factors. The QueryVar is 
    NOT part of the returned ordering'''
    scopes = []
    for f in Factors:
        scopes.append(list(f.get_scope()))
    Vars = []
    for s in scopes:
        for v in s:
            if not v in Vars and v != QueryVar:
                Vars.append(v)
    
    ordering = []
    while Vars:
        (var,new_scope) = min_fill_var(scopes,Vars)
        ordering.append(var)
        if var in Vars:
            Vars.remove(var)
        scopes = remove_var(var, new_scope, scopes)
    return ordering

def min_fill_var(scopes, Vars):
    '''Given a set of scopes (lists of lists of variables) compute and
    return the variable with minimum fill in. That the variable that
    generates a factor of smallest scope when eliminated from the set
    of scopes. Also return the new scope generated from eliminating
    that variable.'''
    minv = Vars[0]
    (minfill,min_new_scope) = compute_fill(scopes,Vars[0])
    for v in Vars[1:]:
        (fill, new_scope) = compute_fill(scopes, v)
        if fill < minfill:
            minv = v
            minfill = fill
            min_new_scope = new_scope
    return (minv, min_new_scope)

def compute_fill(scopes, var):
    '''Return the fill in scope generated by eliminating var from
    scopes along with the size of this new scope'''
    union = []
    for s in scopes:
        if var in s:
            for v in s:
                if not v in union:
                    union.append(v)
    if var in union: union.remove(var)
    return (len(union), union)

def remove_var(var, new_scope, scopes):
    '''Return the new set of scopes that arise from eliminating var
    from scopes'''
    new_scopes = []
    for s in scopes:
        if not var in s:
            new_scopes.append(s)
    new_scopes.append(new_scope)
    return new_scopes
            
        
#
#
##
#####
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

    all_factors = Net.factors()
    length_factors = len(all_factors)
            
    for i in range(length_factors):
        for var in EvidenceVars: #a LIST of Variable objects. 
            factor_scope = all_factors[i].get_scope()
            if var in factor_scope:
                var_evidence = var.get_evidence()
                new_factors = restrict_factor(all_factors[i], var, var_evidence)
                all_factors[i] = new_factors
    
    ordering = min_fill_ordering(all_factors, QueryVar)
    
    for var in ordering:
        multiply_factors_lst = []
        for factor in all_factors:
            if var in factor.get_scope():
                multiply_factors_lst.append(factor)
#                continue
#            
        factors_multiplied = multiply_factors(multiply_factors_lst)
        summed_out_factor = sum_out_variable(factors_multiplied, var)
        
        for factor in multiply_factors_lst: 
            all_factors.remove(factor) #remove if factor in multiply_factors_lst
#        all_factors = [ff for ff in all_factors if ff not in multiply_factors_lst]
        all_factors.append(summed_out_factor)
#        ordering = ordering[1:]
        
    multiplied_factor = multiply_factors(all_factors)
    return normalize(multiplied_factor.values)

import math


if __name__ == "__main__":
    A = Variable('A', ['a', '-a'])
    B = Variable('B', ['b', '-b'])
    C = Variable('C', ['c', '-c'])
    D = Variable('D', ['d', '-d'])
    E = Variable('E', ['e', '-e'])
    F = Variable('F', ['f', '-f'])
    G = Variable('G', ['g', '-g'])
    H = Variable('H', ['h', '-h'])
    I = Variable('I', ['i', '-i'])
    

    FA = Factor('P(A)', [A])
    FA.add_values([['a', 0.9], 
                   ['-a', 0.1]])

    FB = Factor('P(B|A,H)', [B, A, H])
    FB.add_values([['b',  'a',  'h',  1.0],
                   ['b',  'a',  '-h', 0.0], 
                   ['b',  '-a', 'h',  0.5], 
                   ['b',  '-a', '-h', 0.6], 
                   ['-b', 'a',  'h',  0.0], 
                   ['-b', 'a',  '-h', 1.0], 
                   ['-b', '-a', 'h',  0.5], 
                   ['-b', '-a', '-h', 0.4]]) 
          
    FC = Factor('P(C|B,G)', [C, B, G])
    FC.add_values([['c',  'b',  'g',  0.9], 
                   ['c',  'b',  '-g', 0.9], 
                   ['c',  '-b', 'g',  0.1], 
                   ['c',  '-b', '-g', 1.0], 
                   ['-c', 'b',  'g',  0.1], 
                   ['-c', 'b',  '-g', 0.1], 
                   ['-c', '-b', 'g',  0.9], 
                   ['-c', '-b', '-g', 0.0]])
      
    FD = Factor('P(D|C,F)', [D, C, F])
    FD.add_values([['d',  'c',  'f',  0.0], 
                   ['d',  'c',  '-f', 1.0], 
                   ['d',  '-c', 'f',  0.7], 
                   ['d',  '-c', '-f', 0.2], 
                   ['-d', 'c',  'f',  1.0], 
                   ['-d', 'c',  '-f', 0.0], 
                   ['-d', '-c', 'f',  0.3], 
                   ['-d', '-c', '-f', 0.8]])
       
    FE = Factor('P(E|C)', [E, C])
    FE.add_values([['e',  'c',  0.2],
                  ['e',  '-c', 0.4], 
                  ['-e', 'c',  0.8], 
                  ['-e', '-c', 0.6]])       
       
    FF = Factor('P(F)', [F])
    FF.add_values([['f', 0.1],
                   ['-f', 0.9]])
   
    FG = Factor('P(G)', [G])
    FG.add_values([['g', 1.0], 
                   ['-g', 0.0]])
   
    FH = Factor('P(H)', [H])
    FH.add_values([['h', 0.5], 
                   ['-h', 0.5]])
   
    FI = Factor('P(I|B)', [I, B]) 
    FI.add_values([['i',  'b',  0.3], 
               ['i',  '-b',  0.9], 
               ['-i', 'b', 0.7], 
               ['-i', '-b', 0.1]])
       

    BayesNetQ1 = BN('Q1', [A,B,C,D,E,F,G,H,I], [FA,FB,FC,FD,FE,FF,FG,FH,FI])



    factors =  BayesNetQ1.factors()
#    var = BayesNetQ1.variables()
#    print(factors)
#    print(var)
#    m =  map(Factor.get_scope, factors)
#    l = list(m)
#    print(l)
#    ll = (sum(l, []))
#    print(set(ll))
#    for f in factors:
#        print(f.name)
#    name =  "_multiply[" + " + ".join(f.name for f in factors) + "]"
#    print(name)
#    FH.print_table()
    
    
    
    
    A.set_evidence('a')
    q1a = VE(BayesNetQ1, B, [A])
    print("Q1a)")
    print('P(b|a)', q1a[0])
    print('P(-b|a)', q1a[1])
    assert q1a[1] == 1 - q1a[0] #check if complement is 1 - prob

    A.set_evidence('a')
    q1b = VE(BayesNetQ1, C, [A])
    print("")
    print("Q1b)")
    print('P(c|a)', q1b[0])
    print('P(-c|a)', q1b[1])
    assert q1b[1] == 1 - q1b[0] #check if complement is 1 - prob
    
    
    A.set_evidence('a')
    E.set_evidence('-e')
    q1c = VE(BayesNetQ1, C, [A, E])
    print("")
    print("Q1c)")
    print('P(c|a, -e)', q1c[0])
    print('P(-c|a, -e)', q1c[1]) 
    assert math.isclose(q1c[1], 1 - q1c[0]) #check if complement is 1 - prob
       

    A.set_evidence('a')
    F.set_evidence('-f')
    q1d = VE(BayesNetQ1, C, [A, F])
    print("")
    print("Q1d)")
    print('P(c|a, -f)', q1d[0])
    print('P(-c|a, f)', q1d[1]) 
    assert math.isclose(q1d[1], 1 - q1d[0]) #check if complement is 1 - prob

