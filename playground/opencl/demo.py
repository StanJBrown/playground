#!/usr/bin/env python
import pyopencl as cl
import numpy
import numpy.linalg as la


"""
OpenCL has its own basic primitive data types to avoid different data sizes.


Plaforms



Devices



Contexts

Contexts allow OpenCL devices to manage different scenarios to which the device
is performing. It identifies a set of devices, those which are selected, in
order to create a command queue.


Programs, Kernels

Programs and kernels are both executable code, however a kernel only contains a
function to be executed on a device. In contrast, a program is a container of
one or many different kernels.



Command Queues
"""

if __name__ == "__main__":
    a = numpy.random.rand(50000).astype(numpy.float32)
    b = numpy.random.rand(50000).astype(numpy.float32)

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    mf = cl.mem_flags
    a_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=a)
    b_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=b)
    dest_buf = cl.Buffer(ctx, mf.WRITE_ONLY, b.nbytes)

    prg = cl.Program(ctx, """
__kernel void sum(
    __global const float *a,
    __global const float *b,
    __global float *c
)
{
    int gid = get_global_id(0);
    c[gid] = a[gid] + b[gid];
}
    """).build()

    prg.sum(queue, a.shape, None, a_buf, b_buf, dest_buf)

    a_plus_b = numpy.empty_like(a)
    cl.enqueue_copy(queue, a_plus_b, dest_buf)

    print(la.norm(a_plus_b - (a + b)), la.norm(a_plus_b))
