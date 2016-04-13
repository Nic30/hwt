#include "ap_int.h"
#include "hls_stream.h"

#define DW 64

#define DW_B (DW/8)

typedef ap_uint<DW> d_t;
typedef hls::stream<d_t> axi_t;

#define exprStr "SIP:"

unsigned int expr = *((unsigned int *) exprStr);
#define exprSize (sizeof exprStr)

#define BITMASK(bits) ((1L<<(bits))-1))
#define GET_CHARS(val, indx, mask)  ( ((val) >> ((indx) *8)) & (mask) )

void exactMatch(axi_t & din, bool &match, unsigned * patern) {
#pragma HLS INTERFACE s_axilite register port=patern bundle=cfg
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE ap_none port=match
#pragma HLS INTERFACE axis port=din

	d_t data = din.read();
	ap_uint<DW_B - exprSize> m;

	for (int dataI = 0; dataI < DW_B - exprSize; dataI++) {
#pragma HLS UNROLL
		m[dataI] = (expr == GET_CHARS(data, dataI, BITMASK(exprSize*8));
	}

	match = m.or_reduce();
}

int main() {

	return 0;
}
