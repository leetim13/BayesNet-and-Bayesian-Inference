from bnetbase import *
from carDiagnosis import *

if __name__ == '__main__':
    
#Question 2a
#Show a case of conditional independence in the Net where knowing some
#evidence item V1 = d1 makes another evidence item V2 = d2 irrelevant to the probability of
#some third variable V3. (Note that conditional independence requires that the independence
#holds for all values of V3).
    
    #Given evidence of third var, probability is the same = conditional independent
    #P(V3|V1) = P(V3|V1, V2)
    #P(z|x,y) = P(z|y)
    #z = car starts, x = air filter, y = air system
    
    #v1 = air system, v2 = air filter, v3= car starts
    
    asys.set_evidence('okay')
    print("Given asys = " + asys.get_evidence())
    probs = VE(car, st, [asys])
    for i in range(len(probs)):
        print("P({0:} = {1:} | af = clean) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    print()
    
    asys.set_evidence('okay')
    af.set_evidence('clean')
    print("Given asys = " + asys.get_evidence())
    print("Given asys = " + asys.get_evidence())
    probs = VE(car, st, [asys, af])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    print()

    asys.set_evidence('okay')
    af.set_evidence('dirty')
    print("asys = " + asys.get_evidence())
    print("af = " + af.get_evidence())
    probs = VE(car, st, [asys, af])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    print()
    
    asys.set_evidence('faulty')
    print("asys = " + asys.get_evidence())
    probs = VE(car, st, [asys])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    print()

    asys.set_evidence('faulty')
    af.set_evidence('clean')
    print("asys = " + asys.get_evidence())
    print("af = " + af.get_evidence())
    probs = VE(car, st, [asys, af])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    print()

    asys.set_evidence('faulty')
    af.set_evidence('dirty')
    print("asys = " + cs.get_evidence())
    print("af = " + af.get_evidence())
    probs = VE(car, st, [asys, af])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    print()
    
        
    #2b
    #Show a case of conditional independence in the Net where two variables  (V1 and V2)  are
    #independent given NO evidence at a third variable yet dependent given evidence at the third
    #variable.
    #explaining away: want to prove
    #V1 = x = spark plugs
    #V2 = Z =  voltage at plug
    #V3 = evidence = conditioned = y = spark quality
    #P(z|x, y) != P(z|y)
    #x = spark plugs, z = voltage at plug (pv), y = spark quality
    #P(pv|sp, sq) != P(pv|sq)
    
    print("q2b")
    
    #P(pv|sq)
    sq.set_evidence('good')
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sq = good) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('good')
    sp.set_evidence('okay')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
   
    #P(pv|sp, sq) 
    sq.set_evidence('good')
    sp.set_evidence('too_wide')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('good')
    sp.set_evidence('fouled')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #bad
        
    #P(pv|sq)
    sq.set_evidence('bad')
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sq = good) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('bad')
    sp.set_evidence('okay')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('bad')
    sp.set_evidence('too_wide')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('bad')
    sp.set_evidence('fouled')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    
    #sq = very bad
    
    #P(pv|sq)
    sq.set_evidence('very_bad')
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sq = good) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
        #P(pv|sp, sq) 
    sq.set_evidence('very_bad')
    sp.set_evidence('okay')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('very_bad')
    sp.set_evidence('too_wide')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    #P(pv|sp, sq) 
    sq.set_evidence('very_bad')
    sp.set_evidence('fouled')
    print("Given sp = " + sp.get_evidence())
    print("Given sq = " + sq.get_evidence())
    probs = VE(car, pv, [sp, sq])
    for i in range(len(probs)):
        print("P({0:} = {1:} | sp = okay, sq = good ) = {2:0.1f}".format(pv.name, pv.domain()[i], 100*probs[i]))
    print()
    
    
    print("q2c")
    #increases monotonically as we add evidence items
    #Show a sequence of accumulated evidence items V1 = d1,...,V5 = d5
    #(i.e., each evidence item in the sequence is added to the previous evidence items) 
    #such that each additional evidence item *increases* the probability of  some variable V0 having value d0.
    #(That is, the probability of V0 = d0 increases *monotonically* as we add the evidence items).
    #V0= car starts
    #d0= true
    
    #V1 = cc Car cranks
    #d1= true
    
    #V2 = ss starter system
    #d2= okay
    
    #V3 = bv battery voltage
    #d3= strong
    
    #V4 = tm spark timing 
    #d4= good
    
    #V5 =  Voltage at plug pv
    #d5 = strong
    #What is P(V0=d0|V1=d1,V2=d2,V3=d3,V4=d4,V5=d5)? 79.7
    
    probs = VE(car, st, [])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # cc = 'true' increases the probability of 'Car Starts'
    cc.set_evidence('true')
    print("cc = " + cc.get_evidence())
    probs = VE(car, st, [cc])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # ss = 'okay' increases the probability of 'Car Starts'
    cc.set_evidence('true')
    ss.set_evidence('okay')
    print("cc = " + cc.get_evidence())
    print("ss = " + ss.get_evidence())
    probs = VE(car, st, [cc, ss])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # bv = 'strong' increases the probability of 'Car Starts'
    cc.set_evidence('true')
    ss.set_evidence('okay')
    bv.set_evidence('strong')
    print("cc = " + cc.get_evidence())
    print("ss = " + ss.get_evidence())
    print("bv = " + bv.get_evidence())
    probs = VE(car, st, [cc, ss, bv])
    for i in range(len(probs)):
       print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # tm = 'good' increases the probability of 'Car Starts'
    cc.set_evidence('true')
    ss.set_evidence('okay')
    bv.set_evidence('strong')
    tm.set_evidence('good')
    print("cc = " + cc.get_evidence())
    print("ss = " + ss.get_evidence())
    print("bv = " + bv.get_evidence())
    print("tm = " + tm.get_evidence())    
    probs = VE(car, st, [cc, ss, bv, tm])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()
    
    # tm = 'good' increases the probability of 'Car Starts'
    cc.set_evidence('true')
    ss.set_evidence('okay')
    bv.set_evidence('strong')
    tm.set_evidence('good')
    pv.set_evidence('strong')
    print("cc = " + cc.get_evidence())
    print("ss = " + ss.get_evidence())
    print("bv = " + bv.get_evidence())
    print("tm = " + tm.get_evidence())    
    print("pv = " + pv.get_evidence())  
    probs = VE(car, st, [cc, ss, bv, tm, pv])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()
    
    
    
    print("q2d")
#    Show a sequence of accumulated evidence items V1 = d1,...,V5 = d5 
#    (i.e., each evidence item in the sequence is added to the previous evidence items) 
#    such that each additional evidence item decreases the probability of  some variable 
#    V0 having value d0. (That is, the probability of V0 = d0 decreases *monotonically* 
#    as we add the evidence items). *Same as Question 2(c), but decreasing instead of increasing*
    #V0= car starts
    #d0= true
    
    #V1 = asys air system
    #d1= faulty
    
    #V2 = sp Spark plugs
    #d2= fouled 
    
    #V3 = ba battery age 
    #d3= old
    
    #V4 = ds distributer 
    #d4= faulty
    
    #V5 = sm Starter Motor
    #d5 = faulty
#   What is P(V0=d0|V1=d1,V2=d2,V3=d3,V4=d4,V5=d5)? * 0.1
    
    
    
    
    
    probs = VE(car, st, [])
    for i in range(len(probs)):
       print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # cc = 'true' increases the probability of 'Car Starts'
    asys.set_evidence('faulty')
    print("asys = " + asys.get_evidence())
    probs = VE(car, st, [asys])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # ss = 'okay' increases the probability of 'Car Starts'
    asys.set_evidence('faulty')
    sp.set_evidence('fouled')
    print("asys = " + asys.get_evidence())
    print("sp = " + sp.get_evidence())
    probs = VE(car, st, [asys, sp])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # bv = 'strong' increases the probability of 'Car Starts'
    asys.set_evidence('faulty')
    sp.set_evidence('fouled')
    ba.set_evidence('old')
    print("asys = " + asys.get_evidence())
    print("sp = " + sp.get_evidence())
    print("ba = " + ba.get_evidence())
    probs = VE(car, st, [asys, sp, ba])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()

    # tm = 'good' increases the probability of 'Car Starts'
    asys.set_evidence('faulty')
    sp.set_evidence('fouled')
    ba.set_evidence('old')
    ds.set_evidence('faulty')
    print("asys = " + asys.get_evidence())
    print("sp = " + sp.get_evidence())
    print("ba = " + ba.get_evidence())
    print("ds = " + al.get_evidence())    
    probs = VE(car, st, [asys, sp, ba, ds])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()
    
    
    asys.set_evidence('faulty')
    sp.set_evidence('fouled')
    ba.set_evidence('old')
    ds.set_evidence('faulty')
    sm.set_evidence('faulty')
    print("asys = " + asys.get_evidence())
    print("sp = " + sp.get_evidence())
    print("ba = " + ba.get_evidence())
    print("ds = " + ds.get_evidence())  
    print("sm = " + sm.get_evidence())    
    probs = VE(car, st, [asys, sp, ba, ds, sm])
    for i in range(len(probs)):
        print("P({0:} = {1:}) = {2:f}".format(st.name, st.domain()[i], probs[i]))
    print()
    
    
    
    ## Question 2
    ## Voltage at Plug = 'weak' explains away Spark Quality = 'bad'
    ## which decreases the probability of Spark Plugs = 'too wide'
    ## and Spark Plugs = 'fouled'
    #sq.set_evidence('bad')
    #print("sq = " + sq.get_evidence())
    #probs = VE(car, sp, [sq])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(sp.name, sp.domain()[i], 100*probs[i]))
    #print()

    #sq.set_evidence('bad')
    #pv.set_evidence('weak')
    #print("sq = " + sq.get_evidence())
    #print("pv = " + pv.get_evidence())    
    #probs = VE(car, sp, [sq, pv])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(sp.name, sp.domain()[i], 100*probs[i]))
    #print()

    ## Question 3
    #probs = VE(car, st, [])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    #print()

    ## asys = 'okay' increases the probability of 'Car Starts'
    #asys.set_evidence('okay')
    #print("asys = " + asys.get_evidence())
    #probs = VE(car, st, [asys])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    #print()

    ## fs = 'okay' increases the probability of 'Car Starts'
    #asys.set_evidence('okay')
    #fs.set_evidence('okay')
    #print("asys = " + asys.get_evidence())
    #print("fs = " + fs.get_evidence())
    #probs = VE(car, st, [asys, fs])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    #print()

    ## cc = 'true' increases the probability of 'Car Starts'
    #asys.set_evidence('okay')
    #fs.set_evidence('okay')
    #cc.set_evidence('true')
    #print("asys = " + asys.get_evidence())
    #print("fs = " + fs.get_evidence())
    #print("cc = " + cc.get_evidence())
    #probs = VE(car, st, [asys, fs, cc])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    #print()

    ## sq = 'good' increases the probability of 'Car Starts'
    #asys.set_evidence('okay')
    #fs.set_evidence('okay')
    #cc.set_evidence('true')
    #sq.set_evidence('good')
    #print("asys = " + asys.get_evidence())
    #print("fs = " + fs.get_evidence())
    #print("cc = " + cc.get_evidence())
    #print("sq = " + sq.get_evidence())    
    #probs = VE(car, st, [asys, fs, cc, sq])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(st.name, st.domain()[i], 100*probs[i]))
    #print()

    ## Question 4
    #probs = VE(car, cc, [])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(cc.name, cc.domain()[i], 100*probs[i]))
    #print()

    ## h1 = 'off' decreases the probability of 'Car Cranks'
    #hl.set_evidence('off')
    #print("h1 = " + hl.get_evidence())
    #probs = VE(car, cc, [hl])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(cc.name, cc.domain()[i], 100*probs[i]))
    #print()

    ## cs = 'faulty' decreases the probability of 'Car Cranks'
    #hl.set_evidence('off')
    #cs.set_evidence('faulty')
    #print("h1 = " + hl.get_evidence())
    #print("cs = " + cs.get_evidence())
    #probs = VE(car, cc, [hl, cs])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(cc.name, cc.domain()[i], 100*probs[i]))
    #print()

    ## bv = 'strong' increases the probability of 'Car Cranks'
    #hl.set_evidence('off')
    #cs.set_evidence('faulty')
    #bv.set_evidence('strong')
    #print("h1 = " + hl.get_evidence())
    #print("cs = " + cs.get_evidence())
    #print("bv = " + bv.get_evidence())
    #probs = VE(car, cc, [hl, cs, bv])
    #for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(cc.name, cc.domain()[i], 100*probs[i]))
    #print()

    ## ss = 'okay' increases the probability of 'Car Cranks'
    #hl.set_evidence('off')
#    cs.set_evidence('faulty')
#    bv.set_evidence('strong')
#    ss.set_evidence('okay')
#    print("h1 = " + hl.get_evidence())
#    print("cs = " + cs.get_evidence())
#    print("bv = " + bv.get_evidence())
#    print("ss = " + ss.get_evidence())
#    probs = VE(car, cc, [hl, cs, bv, ss])
#    for i in range(len(probs)):
        #print("P({0:} = {1:}) = {2:0.1f}".format(cc.name, cc.domain()[i], 100*probs[i]))
    #print()
