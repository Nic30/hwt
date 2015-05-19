------------------------------------------------------
 -- A four level, round-robin arbiter. This was 
 -- orginally coded by WD Peterson in VHDL. 
 -- Coder       : Deepak Kumar Tala (Verilog) 
 -- Translator  : Alexander H Pham (VHDL) 
 ------------------------------------------------------
 library ieee;
     use ieee.std_logic_1164.all;
 
 entity arbiter is
     port (
         clk,  rst  :in  std_logic;
         req0, req1 :in  std_logic;
         req2, req3 :in  std_logic;
         gnt0, gnt1 :out std_logic;
         gnt2, gnt3 :out std_logic
     );
 end entity;
 architecture behavior of arbiter is
 
    ----------------Internal Registers-----------------
     signal gnt,    lgnt    :std_logic_vector (1 downto 0);
     signal comreq, lcomreq :std_logic;
     signal beg,    ledge   :std_logic;
     signal lgnt0,  lgnt1   :std_logic;
     signal lgnt2,  lgnt3   :std_logic;
     signal lmask0, lmask1  :std_logic;
     signal lasmask         :std_logic;
 
 begin
 
    ----------------Code Starts Here------------------
     process (clk) 
     begin
         if (rising_edge(clk)) then
             if (rst = '1') then
                 lgnt0 <= '0';
                 lgnt1 <= '0';
                 lgnt2 <= '0';
                 lgnt3 <= '0';
             else
                 lgnt0 <=(not lcomreq and not lmask1 and not lmask0 and
                          not req3 and not req2 and not req1 and req0)
                      or (not lcomreq and not lmask1 and lmask0 and
                          not req3 and not req2 and req0)
                      or (not lcomreq and lmask1 and not lmask0 and
                          not req3 and req0)
                      or (not lcomreq and lmask1 and lmask0 and req0)
                      or (lcomreq and lgnt0);
                      
                 lgnt1 <=(not lcomreq and not lmask1 and not lmask0 and req1)
                      or (not lcomreq and not lmask1 and lmask0 and
                          not req3 and not req2 and req1 and not req0)
                      or (not lcomreq and lmask1 and not lmask0 and
                          not req3 and req1 and not req0)
                      or (not lcomreq and lmask1 and lmask0 and
                              req1 and not req0)
                      or (lcomreq and lgnt1);
                      
                 lgnt2 <=(not lcomreq and not lmask1 and not lmask0 and
                              req2 and not req1)
                      or (not lcomreq and not lmask1 and lmask0 and req2)
                      or (not lcomreq and lmask1 and not lmask0 and
                          not req3 and req2 and not req1 and not req0)
                      or (not lcomreq and lmask1 and lmask0 and
                              req2 and not req1 and not req0)
                      or (lcomreq and lgnt2);
                      
                 lgnt3 <=(not lcomreq and not lmask1 and not lmask0 and
                              req3 and not req2 and not req1)
                      or (not lcomreq and not lmask1 and lmask0 and
                              req3 and not req2)
                      or (not lcomreq and lmask1 and not lmask0 and req3)
                      or (not lcomreq and lmask1 and lmask0 and
                              req3 and not req2 and not req1 and not req0)
                      or (lcomreq and lgnt3);
             end if;
         end if;
     end process;
 
   ------------------------------------------------------
   -- lasmask state machine.
   ------------------------------------------------------
    beg <= (req3 or req2 or req1 or req0) and not lcomreq;
    process (clk) 
    begin
        if (rising_edge(clk)) then
            lasmask <= (beg and not ledge and not lasmask);
            ledge   <= (beg and not ledge and     lasmask)
                   or  (beg and     ledge and not lasmask);
        end if;
    end process;

   ------------------------------------------------------
   -- comreq logic.
   ------------------------------------------------------
    lcomreq <= (req3 and lgnt3)
            or (req2 and lgnt2)
            or (req1 and lgnt1)
            or (req0 and lgnt0);

   ------------------------------------------------------
   -- Encoder logic.
   ------------------------------------------------------
    lgnt <=  ((lgnt3 or lgnt2) & (lgnt3 or lgnt1));

   ------------------------------------------------------
   -- lmask register.
   ------------------------------------------------------
    process (clk) 
    begin
        if (rising_edge(clk)) then
            if (rst = '1') then
                lmask1 <= '0';
                lmask0 <= '0';
            elsif (lasmask = '1') then
                lmask1 <= lgnt(1);
                lmask0 <= lgnt(0);
            else
                lmask1 <= lmask1;
                lmask0 <= lmask0;
            end if;
        end if;
    end process;

    comreq <= lcomreq;
    gnt    <= lgnt;
   ------------------------------------------------------
   -- Drive the outputs
   ------------------------------------------------------
    gnt3   <= lgnt3;
    gnt2   <= lgnt2;
    gnt1   <= lgnt1;
    gnt0   <= lgnt0;

end architecture;

------------------------------------------------------
-- Arbiter test bench
------------------------------------------------------
library ieee;
    use ieee.std_logic_1164.all;
    use ieee.std_logic_unsigned.all;
    use ieee.std_logic_textio.all;
    use std.textio.all;

entity arbiter_tb is
end entity;
architecture test of arbiter_tb is
    signal clk        :std_logic := '0';
    signal rst        :std_logic := '1';
    signal req0, req1 :std_logic := '0';
    signal req2, req3 :std_logic := '0';
    signal gnt0, gnt1 :std_logic := '0';
    signal gnt2, gnt3 :std_logic := '0';
    
    component arbiter is
    port (
        clk,  rst  :in  std_logic;
        req0, req1 :in  std_logic;
        req2, req3 :in  std_logic;
        gnt0, gnt1 :out std_logic;
        gnt2, gnt3 :out std_logic
    );
    end component;
    
    constant PERIOD :time := 20 ns;

begin
   -- Clock generator
    clk <= not clk after PERIOD/2;
    rst <= '0'     after PERIOD;
    
    req0 <= '1' after PERIOD*1, '0' after PERIOD*2,
            '1' after PERIOD*3, '0' after PERIOD*7;

    req1 <= '1' after PERIOD*3, '0' after PERIOD*4;

    req2 <= '1' after PERIOD*4, '0' after PERIOD*5;

    req3 <= '1' after PERIOD*5, '0' after PERIOD*6;

   -- Connect the DUT
    Inst_arbiter : arbiter
    port map (
        clk  => clk,
        rst  => rst,
        req0 => req0,
        req1 => req1,
        req2 => req2,
        req3 => req3,
        gnt0 => gnt0,
        gnt1 => gnt1,
        gnt2 => gnt2,
        gnt3 => gnt3
    );

end architecture;
