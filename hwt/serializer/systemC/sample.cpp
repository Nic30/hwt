#include <Python.h>
#include <systemc.h>

SC_MODULE(nand2)          // declare nand2 sc_module
{
	sc_in<bool> A, B;       // input signal ports
	sc_out<bool> F;         // output signal ports

	void do_nand2()         // a C++ function
	{
		F.write(!(A.read() && B.read()));
	}

	SC_CTOR(nand2)          // constructor for nand2
	{
		SC_METHOD(do_nand2);  // register do_nand2 with kernel
		sensitive << A << B;// sensitivity list
	}
};

SC_MODULE(exor2)
{
	sc_in<bool> A, B;
	sc_out<bool> F;

	nand2 n1, n2, n3, n4;

	sc_signal<bool> S1, S2, S3;

	SC_CTOR(exor2) : n1("N1"), n2("N2"), n3("N3"), n4("N4")
	{
		n1.A(A);
		n1.B(B);
		n1.F(S1);

		n2.A(A);
		n2.B(S1);
		n2.F(S2);

		n3.A(S1);
		n3.B(B);
		n3.F(S3);

		n4.A(S2);
		n4.B(S3);
		n4.F(F);
	}
};

SC_MODULE(stim)
{
	sc_out<bool> A, B;
	sc_in<bool> Clk;

	void StimGen() {
		A.write(false);
		B.write(false);
		wait();
		A.write(false);
		B.write(true);
		wait();
		A.write(true);
		B.write(false);
		wait();
		A.write(true);
		B.write(true);
		wait();
		sc_stop();
	}
	SC_CTOR(stim)
	{
		SC_THREAD(StimGen);
		sensitive << Clk.pos();
	}
};

SC_MODULE(mon)
{
	sc_in_clk Clk;
	sc_in<bool> A, B, F;
	void prc_monitor() {
		cout << " At " << sc_simulation_time() << " input is : ";
		cout << A << " , " << B << " output is : " << F << endl;
	}

	SC_CTOR(mon)
	{

		SC_METHOD(prc_monitor);
		sensitive << Clk.pos();
	}
};

int sc_main(int argc, char* argv[]) {
	sc_signal<bool> ASig, BSig, FSig;
	sc_clock TestClk("TestClock", 10, SC_NS, 0.5);

	stim Stim1("Stimulus");
	Stim1.A(ASig);
	Stim1.B(BSig);
	Stim1.Clk(TestClk);

	exor2 DUT("exor2");
	DUT.A(ASig);
	DUT.B(BSig);
	DUT.F(FSig);

	mon Monitor1("Monitor");
	Monitor1.A(ASig);
	Monitor1.B(BSig);
	Monitor1.F(FSig);
	Monitor1.Clk(TestClk);

	sc_start();  // run forever

	return 0;

}

static PyObject *
keywdarg_parrot(PyObject *self, PyObject *args, PyObject *keywds) {
	int voltage;
	const char *state = "a stiff";
	const char *action = "voom";
	const char *type = "Norwegian Blue";

	static char * kwlist[] = { (char *)"voltage", (char *)"state", (char *)"action", (char *)"type", NULL };

	if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|sss", kwlist, &voltage,
			&state, &action, &type))
		return NULL;

	printf("-- This parrot wouldn't %s if you put %i Volts through it.\n",
			action, voltage);
	printf("-- Lovely plumage, the %s -- It's %s!\n", type, state);

	Py_RETURN_NONE;
}

static PyMethodDef keywdarg_methods[] = {
    /* The cast of the function is necessary since PyCFunction values
     * only take two PyObject* parameters, and keywdarg_parrot() takes
     * three.
     */
    {"parrot", (PyCFunction)keywdarg_parrot, METH_VARARGS | METH_KEYWORDS,
	 "Print a lovely skit to standard output."},
    {NULL, NULL, 0, NULL}   /* sentinel */
};

static struct PyModuleDef keywdargmodule = {
    PyModuleDef_HEAD_INIT,
    "keywdarg",
    NULL,
    -1,
    keywdarg_methods
};

PyMODINIT_FUNC PyInit_keywdarg(void) {
	return PyModule_Create(&keywdargmodule);
}
