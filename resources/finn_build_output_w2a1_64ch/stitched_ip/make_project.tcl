create_project finn_vivado_stitch_proj /tmp/finn_dev_jokar/vivado_stitch_proj_yys_82a9 -part xc7a200t
set_property ip_repo_paths [list /workspace/finn/finn-rtllib/memstream /tmp/finn_dev_jokar/code_gen_ipgen_StreamingFIFO_0_ob5dtyc4/project_StreamingFIFO_0/sol1/impl/verilog /tmp/finn_dev_jokar/code_gen_ipgen_FMPadding_Batch_0_en055bjd/project_FMPadding_Batch_0/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_ConvolutionInputGenerator1D_0_m5yr2c57/project_ConvolutionInputGenerator1D_0/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_0_r2l81l2y/project_StreamingFCLayer_Batch_0/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_FMPadding_Batch_1_vns69xzw/project_FMPadding_Batch_1/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_ConvolutionInputGenerator1D_1_9ail67l6/project_ConvolutionInputGenerator1D_1/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_1_jyi0q7y_/project_StreamingFCLayer_Batch_1/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_FMPadding_Batch_2_5w5u75bw/project_FMPadding_Batch_2/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_ConvolutionInputGenerator1D_2_abhj22xn/project_ConvolutionInputGenerator1D_2/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_2_aqd1y8fw/project_StreamingFCLayer_Batch_2/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_FMPadding_Batch_3_3dfii6cu/project_FMPadding_Batch_3/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_ConvolutionInputGenerator1D_3_4k0xkhzr/project_ConvolutionInputGenerator1D_3/sol1/impl/ip /tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_3_lw7df92t/project_StreamingFCLayer_Batch_3/sol1/impl/ip] [current_project]
update_ip_catalog
create_bd_design "finn_design"
create_bd_cell -type ip -vlnv xilinx.com:hls:StreamingFIFO_0:1.0 StreamingFIFO_0
create_bd_cell -type ip -vlnv xilinx.com:hls:FMPadding_Batch_0:1.0 FMPadding_Batch_0
create_bd_cell -type ip -vlnv xilinx.com:hls:ConvolutionInputGenerator1D_0:1.0 ConvolutionInputGenerator1D_0
create_bd_cell -type hier StreamingFCLayer_Batch_0
create_bd_pin -dir I -type clk /StreamingFCLayer_Batch_0/ap_clk
create_bd_pin -dir I -type rst /StreamingFCLayer_Batch_0/ap_rst_n
create_bd_intf_pin -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_0/out_V_V
create_bd_intf_pin -mode Slave -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_0/in0_V_V
create_bd_cell -type ip -vlnv xilinx.com:hls:StreamingFCLayer_Batch_0:1.0 /StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0
create_bd_cell -type ip -vlnv xilinx.com:user:memstream:1.0 /StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0_wstrm
set_property -dict [list CONFIG.NSTREAMS {1} CONFIG.MEM_DEPTH {1} CONFIG.MEM_WIDTH {96} CONFIG.MEM_INIT {/tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_0_r2l81l2y/} CONFIG.RAM_STYLE {auto} CONFIG.STRM0_DEPTH {1} CONFIG.STRM0_WIDTH {96} CONFIG.STRM0_OFFSET {0} ] [get_bd_cells /StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0_wstrm]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0_wstrm/m_axis_0] [get_bd_intf_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0/weights_V_V]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_0/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0_wstrm/aresetn]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_0/ap_clk] [get_bd_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0_wstrm/aclk]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_0/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0/ap_rst_n]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_0/ap_clk] [get_bd_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_0/in0_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0/in0_V_V]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_0/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_0/StreamingFCLayer_Batch_0/out_V_V]
save_bd_design
create_bd_cell -type ip -vlnv xilinx.com:hls:FMPadding_Batch_1:1.0 FMPadding_Batch_1
create_bd_cell -type ip -vlnv xilinx.com:hls:ConvolutionInputGenerator1D_1:1.0 ConvolutionInputGenerator1D_1
create_bd_cell -type hier StreamingFCLayer_Batch_1
create_bd_pin -dir I -type clk /StreamingFCLayer_Batch_1/ap_clk
create_bd_pin -dir I -type rst /StreamingFCLayer_Batch_1/ap_rst_n
create_bd_intf_pin -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_1/out_V_V
create_bd_intf_pin -mode Slave -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_1/in0_V_V
create_bd_cell -type ip -vlnv xilinx.com:hls:StreamingFCLayer_Batch_1:1.0 /StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1
create_bd_cell -type ip -vlnv xilinx.com:user:memstream:1.0 /StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1_wstrm
set_property -dict [list CONFIG.NSTREAMS {1} CONFIG.MEM_DEPTH {1} CONFIG.MEM_WIDTH {768} CONFIG.MEM_INIT {/tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_1_jyi0q7y_/} CONFIG.RAM_STYLE {auto} CONFIG.STRM0_DEPTH {1} CONFIG.STRM0_WIDTH {768} CONFIG.STRM0_OFFSET {0} ] [get_bd_cells /StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1_wstrm]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1_wstrm/m_axis_0] [get_bd_intf_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1/weights_V_V]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_1/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1_wstrm/aresetn]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_1/ap_clk] [get_bd_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1_wstrm/aclk]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_1/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1/ap_rst_n]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_1/ap_clk] [get_bd_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_1/in0_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1/in0_V_V]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_1/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_1/StreamingFCLayer_Batch_1/out_V_V]
save_bd_design
create_bd_cell -type ip -vlnv xilinx.com:hls:FMPadding_Batch_2:1.0 FMPadding_Batch_2
create_bd_cell -type ip -vlnv xilinx.com:hls:ConvolutionInputGenerator1D_2:1.0 ConvolutionInputGenerator1D_2
create_bd_cell -type hier StreamingFCLayer_Batch_2
create_bd_pin -dir I -type clk /StreamingFCLayer_Batch_2/ap_clk
create_bd_pin -dir I -type rst /StreamingFCLayer_Batch_2/ap_rst_n
create_bd_intf_pin -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_2/out_V_V
create_bd_intf_pin -mode Slave -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_2/in0_V_V
create_bd_cell -type ip -vlnv xilinx.com:hls:StreamingFCLayer_Batch_2:1.0 /StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2
create_bd_cell -type ip -vlnv xilinx.com:user:memstream:1.0 /StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2_wstrm
set_property -dict [list CONFIG.NSTREAMS {1} CONFIG.MEM_DEPTH {1} CONFIG.MEM_WIDTH {768} CONFIG.MEM_INIT {/tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_2_aqd1y8fw/} CONFIG.RAM_STYLE {auto} CONFIG.STRM0_DEPTH {1} CONFIG.STRM0_WIDTH {768} CONFIG.STRM0_OFFSET {0} ] [get_bd_cells /StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2_wstrm]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2_wstrm/m_axis_0] [get_bd_intf_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2/weights_V_V]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_2/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2_wstrm/aresetn]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_2/ap_clk] [get_bd_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2_wstrm/aclk]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_2/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2/ap_rst_n]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_2/ap_clk] [get_bd_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_2/in0_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2/in0_V_V]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_2/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_2/StreamingFCLayer_Batch_2/out_V_V]
save_bd_design
create_bd_cell -type ip -vlnv xilinx.com:hls:FMPadding_Batch_3:1.0 FMPadding_Batch_3
create_bd_cell -type ip -vlnv xilinx.com:hls:ConvolutionInputGenerator1D_3:1.0 ConvolutionInputGenerator1D_3
create_bd_cell -type hier StreamingFCLayer_Batch_3
create_bd_pin -dir I -type clk /StreamingFCLayer_Batch_3/ap_clk
create_bd_pin -dir I -type rst /StreamingFCLayer_Batch_3/ap_rst_n
create_bd_intf_pin -mode Master -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_3/out_V_V
create_bd_intf_pin -mode Slave -vlnv xilinx.com:interface:axis_rtl:1.0 /StreamingFCLayer_Batch_3/in0_V_V
create_bd_cell -type ip -vlnv xilinx.com:hls:StreamingFCLayer_Batch_3:1.0 /StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3
create_bd_cell -type ip -vlnv xilinx.com:user:memstream:1.0 /StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3_wstrm
set_property -dict [list CONFIG.NSTREAMS {1} CONFIG.MEM_DEPTH {1} CONFIG.MEM_WIDTH {96} CONFIG.MEM_INIT {/tmp/finn_dev_jokar/code_gen_ipgen_StreamingFCLayer_Batch_3_lw7df92t/} CONFIG.RAM_STYLE {auto} CONFIG.STRM0_DEPTH {1} CONFIG.STRM0_WIDTH {96} CONFIG.STRM0_OFFSET {0} ] [get_bd_cells /StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3_wstrm]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3_wstrm/m_axis_0] [get_bd_intf_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3/weights_V_V]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_3/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3_wstrm/aresetn]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_3/ap_clk] [get_bd_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3_wstrm/aclk]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_3/ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3/ap_rst_n]
connect_bd_net [get_bd_pins StreamingFCLayer_Batch_3/ap_clk] [get_bd_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_3/in0_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3/in0_V_V]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_3/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_3/StreamingFCLayer_Batch_3/out_V_V]
save_bd_design
make_bd_pins_external [get_bd_pins StreamingFIFO_0/ap_clk]
set_property name ap_clk [get_bd_ports ap_clk_0]
make_bd_pins_external [get_bd_pins StreamingFIFO_0/ap_rst_n]
set_property name ap_rst_n [get_bd_ports ap_rst_n_0]
make_bd_intf_pins_external [get_bd_intf_pins StreamingFIFO_0/in0_V_V]
set_property name s_axis_0 [get_bd_intf_ports in0_V_V_0]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins FMPadding_Batch_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins FMPadding_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_0/out_V_V] [get_bd_intf_pins FMPadding_Batch_0/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator1D_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator1D_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins FMPadding_Batch_0/out_V_V] [get_bd_intf_pins ConvolutionInputGenerator1D_0/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFCLayer_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator1D_0/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_0/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins FMPadding_Batch_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins FMPadding_Batch_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_0/out_V_V] [get_bd_intf_pins FMPadding_Batch_1/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator1D_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator1D_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins FMPadding_Batch_1/out_V_V] [get_bd_intf_pins ConvolutionInputGenerator1D_1/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFCLayer_Batch_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator1D_1/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_1/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins FMPadding_Batch_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins FMPadding_Batch_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_1/out_V_V] [get_bd_intf_pins FMPadding_Batch_2/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator1D_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator1D_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins FMPadding_Batch_2/out_V_V] [get_bd_intf_pins ConvolutionInputGenerator1D_2/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFCLayer_Batch_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator1D_2/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_2/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins FMPadding_Batch_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins FMPadding_Batch_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFCLayer_Batch_2/out_V_V] [get_bd_intf_pins FMPadding_Batch_3/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator1D_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator1D_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins FMPadding_Batch_3/out_V_V] [get_bd_intf_pins ConvolutionInputGenerator1D_3/in0_V_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFCLayer_Batch_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFCLayer_Batch_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator1D_3/out_V_V] [get_bd_intf_pins StreamingFCLayer_Batch_3/in0_V_V]
make_bd_intf_pins_external [get_bd_intf_pins StreamingFCLayer_Batch_3/out_V_V]
set_property name m_axis_0 [get_bd_intf_ports out_V_V_0]
set_property CONFIG.FREQ_HZ 100000000.000000 [get_bd_ports /ap_clk]
regenerate_bd_layout
validate_bd_design
save_bd_design
make_wrapper -files [get_files /tmp/finn_dev_jokar/vivado_stitch_proj_yys_82a9/finn_vivado_stitch_proj.srcs/sources_1/bd/finn_design/finn_design.bd] -top
add_files -norecurse /tmp/finn_dev_jokar/vivado_stitch_proj_yys_82a9/finn_vivado_stitch_proj.srcs/sources_1/bd/finn_design/hdl/finn_design_wrapper.v
ipx::package_project -root_dir /tmp/finn_dev_jokar/vivado_stitch_proj_yys_82a9/ip -vendor xilinx_finn -library finn -taxonomy /UserIP -module finn_design -import_files
set_property core_revision 2 [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
ipx::create_xgui_files [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
set_property value_resolve_type user [ipx::get_bus_parameters -of [ipx::get_bus_interfaces -of [ipx::current_core ]]]
ipx::update_checksums [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
ipx::save_core [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
set all_v_files [get_files -filter {FILE_TYPE == Verilog && USED_IN_SYNTHESIS == 1} ]
set fp [open /tmp/finn_dev_jokar/vivado_stitch_proj_yys_82a9/all_verilog_srcs.txt w]
foreach vf $all_v_files {puts $fp $vf}
close $fp
