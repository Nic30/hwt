HWT Circuit normal form (hwtCircuitNF)
======================================

HWT Circuit normal form (hwtCircuitNF) is a format of the netlist which is meant as a most simple and compact format of netlist
for circuit analysis. It is supposed to be human and programmatically readable.

hwtCircuitNF is not dependent on HWT and it is rather a specification of the code-style in Verilog/VHDL.
It specifies how statements and signals should be used in order to reduce number of possible descriptions of the same thing.

E.g. a multiplexer can be described using assignment with indexed/conditional expr. and also using switch/if statement
among other possibilities.
A typical synthesis tool converts all this to a gates and it performs the further code analysis there.
However if we want to perform circuit analysis on statement level we have to check every possible syntax.

By performing code analysis and optimization in place on syntax level on normalized circuit we can gain these advantages:

* No need for further conversions with nice object traceability.
* All optimizations would be nearly human readable in every step.
* There is probably less objects in the circuit which would also improve the performance of the compiler.

However there are also downsides of this approach:

* Object have a complex internal structure which could cancel out performance gains.
* The properties of hwtCircuitNF have to be maintained during the updates which add another performance hits.
* For an efficient implementation of analysis the object have to


hwtCircuitNF rules
------------------

(A definition of common netlist in EDIF/VHDL/SystemVerilog)
The netlist described in hwtCircuitNF is a set of components, statements and signals connecting them.
The signal can not cross the boundary of the component, instead it has to be connected to IO of component to achieve this functionality.
The components can be nested, each component has only a single parent, same applies to statements.
Statement can not have nested component.

(A hwtCircuitNF addition)
The signal is driven from component IO or from statement. The signal endpoint is a component IO or statement which is using this
signal to drive something else. Each signal has to drive something and has to be driven by something.

This implies:

* hwtCircuitNF does not contain unconnected statements/components.
* Each signal is somehow connected to some output of the top.

In addition there are several additional rules about statement syntax and signal usage.


Multiplexer coding style
^^^^^^^^^^^^^^^^^^^^^^^^

Rationale: To avoid expression analysis during detection of enclosures, muxes and latches.

no
.. code-block:: verilog

    x <= y[(i + 1)*8 - 1: i*8];

no
.. code-block:: verilog

    x <= i == 0 ? y[8-1:0] : y[16-1:8];

yes
.. code-block:: verilog

   if (i == 0)
       x <= y[ 8 - 1: 0]
   else if (i == 1)
       x <= y[16 - 1: 8]
   // ...

yes, prefered
.. code-block:: verilog

   case (i)
     1'b0: x <= y[ 8-1:0];
     1'b1: x <= y[16-1:8];

Note that the instanciation of the MUX as a component is not a MUX description.


Const indexed assignment vs assignment of concatenation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rationale: Merge all drivers of signal in to a single statement.


no
.. code-block:: verilog

    s[1] <= y;
    s[0] <= x;

yes - all assignment with a constant part specification converted to an assignment of concatenation of all parts
.. code-block:: verilog

    s <= {y, x};

yes - there is only a single part and this is actually a cast
.. code-block:: verilog

   wire s[0:0];
   s[0] <= y;


Const indexed drives of disjunctive parts of same signal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rationale: Split independent parts of signal if possible.


no
.. code-block:: verilog

    if (c0)
        s[0] <= x;
    if (c1)
        s[1] <= y;


yes - all separately driven parts of signal extracted as a signal and the original signal is driven from its parts
.. code-block:: verilog

    wire s_0_tmp;
    wire s_1_tmp;
    assign s <= {s_1_tmp, s_0_tmp};
    if (c0)
        s_0_tmp <= x;
    if (c1)
        s_1_tmp <= y;

yes - the part specifier is not a constant expression
.. code-block:: verilog

    if (c0)
        s[i][0] <= x;
    if (c1)
        s[i][1] <= y;



Enclosure filed
^^^^^^^^^^^^^^^

Rationale: To be able to analyze any statement without the need for an information from its parent.

no
.. code-block:: verilog
    s <= x0;
    if (c0)
        if (c1) begin
            s <= x1;
        end
    else if (c2)
        s <= x2;


yes - enclosure filled
.. code-block:: verilog
    if (c0)
        if (c1) begin
            s <= x1;
        end else begin
            s <= x0;
        end
    else if (c2)
        s <= x2;
    else
        s <= x0;


Assignment to concatenation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Rationale: To have assignments with a single output and to be able to separate them from statements easily.

no
.. code-block:: verilog
    {a, b} <= {c, d};


yes - assignment only to single destination
.. code-block:: verilog
    a <= c;
    b <= d;



