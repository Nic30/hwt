library ieee; use ieee.std_logic_1164.all, ieee.numeric_std.all;
library tauhop; use tauhop.tlm.all, tauhop.axiTLM.all;

entity axiBfmMaster is
	port(aclk,n_areset:in std_ulogic;
		readRequest,writeRequest:in t_bfm:=((others=>'X'),(others=>'X'),false);
		readResponse,writeResponse:buffer t_bfm;						
		axiMaster_in:in t_axi4StreamTransactor_s2m;
		axiMaster_out:buffer t_axi4StreamTransactor_m2s;
		
		symbolsPerTransfer:in t_cnt;
		outstandingTransactions:buffer t_cnt;
		
		dbg_axiTxFsm:out axiBfmStatesTx:=idle
	);
end entity axiBfmMaster;

architecture rtl of axiBfmMaster is
	signal axiTxState,next_axiTxState:axiBfmStatesTx:=idle;
	
	signal i_readRequest:t_bfm:=((others=>'0'),(others=>'0'),false);
	signal i_writeRequest:t_bfm:=((others=>'0'),(others=>'0'),false);
	
	signal i_readResponse,i_writeResponse:t_bfm;
	
begin
	process(n_areset,symbolsPerTransfer,aclk) is begin
		if falling_edge(aclk) then
			if not n_areset then outstandingTransactions<=symbolsPerTransfer;
			else
				if outstandingTransactions<1 then
					outstandingTransactions<=symbolsPerTransfer;
					report "No more pending transactions." severity note;
				elsif axiMaster_in.tReady then outstandingTransactions<=outstandingTransactions-1;
				end if;
			end if;
		end if;
	end process;
	
	axi_bfmTx_ns: process(all) is begin
		axiTxState<=next_axiTxState;
		
		if not n_areset then axiTxState<=idle;
		else
			case next_axiTxState is
				when idle=>
					if writeRequest.trigger xor i_writeRequest.trigger then axiTxState<=payload; end if;
				when payload=>
					if outstandingTransactions<1 then axiTxState<=endOfTx; end if;
				when endOfTx=>
					axiTxState<=idle;
				when others=>axiTxState<=idle;
			end case;
		end if;
	end process axi_bfmTx_ns;
	
	axi_bfmTx_op: process(all) is begin
		i_writeResponse<=writeResponse;
		
		axiMaster_out.tValid<=false;
		axiMaster_out.tLast<=false;
		axiMaster_out.tData<=(others=>'Z');
		i_writeResponse.trigger<=false;
		
		if writeRequest.trigger xor i_writeRequest.trigger then
			axiMaster_out.tData<=writeRequest.message;
			axiMaster_out.tValid<=true;
		end if;
		
		if not n_areset then axiMaster_out.tData<=(others=>'Z');
		else
			case next_axiTxState is
				when payload=>
					axiMaster_out.tData<=writeRequest.message;
					axiMaster_out.tValid<=true;
					
					if axiMaster_in.tReady then
						i_writeResponse.trigger<=true;
					end if;
					
					if outstandingTransactions<1 then axiMaster_out.tLast<=true; end if;
				when others=> null;
			end case;
		end if;
	end process axi_bfmTx_op;
	
	process(n_areset,aclk) is begin
		if falling_edge(aclk) then
			next_axiTxState<=axiTxState;
			i_writeRequest<=writeRequest;
		end if;
	end process;
	
	process(aclk) is begin
		if rising_edge(aclk) then
			writeResponse<=i_writeResponse;
		end if;
	end process;
	
	dbg_axiTxFSM<=axiTxState;
end architecture rtl;
