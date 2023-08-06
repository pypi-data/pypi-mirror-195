import liblip as ll
import sys
import math
import random
import timeit
import numpy as np

    
# test function, here just a product of sin(2x)sin(2y),...
def fun2( dat, dim):
    s = 1.0
    for j in range( dim): s *= math.sin( 2 * dat[j])
    return s

# generate data randomly
def generate_random_data( dim, npts):
    x, XData, YData = ll.init( dim, npts)
    for i in range( npts):
        for j in range( dim):
            x[j] = random.random() * 3.0
            XData[i * dim + j] = x[j]
        YData[i] = fun2( x, dim)
    return x, XData, YData


def test_slip_int():   
    print( "initializing") 
    dim = 20        # the dimension and size of the data set
    npts = 100000
    LipConst = 0.03
    x, XData, YData = generate_random_data( dim, npts)
    print( f'x: {len( x)}, XData: {len( XData)}, YData: {len( YData) }')

    for j in range( dim): x[j]=random.random() * 3.0 # some random x
    # calculate the value
    index = [0] * npts
    print( "calculating")
    XData = np.ascontiguousarray( XData, dtype = 'float64')
    YData = np.ascontiguousarray( YData, dtype = 'float64')
    x = np.ascontiguousarray( x, dtype = 'float64')
    
    t0 = timeit.default_timer()
    print( f'x: {id( x)}, XData: {id( XData)}, YData: {id( YData) }')
    w = ll.LipIntValue( dim,npts,x,XData, YData,LipConst,index)
    print( f'x: {id( x)}, XData: {id( XData)}, YData: {id( YData) }')
    t1 = timeit.default_timer()   
    print( "time: ", t1 - t0)
    print( "w: ", w)

###
# Main test program
###
if __name__ == "__main__":
    print( "-- test wrapper start --")
    test_slip_int()
    print( "-- test wrapper end --")
