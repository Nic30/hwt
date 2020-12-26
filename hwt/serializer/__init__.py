"""
This package contains serializers. Purpose of serializer class
is to convert hwt representations of designed architecture
to hdlConvertorAst to convert it to target language (VHDL/Verilog/SystemC...+xdc/ucf/...).

Rather than using serializer classes manually it is recommended to use :func:`hwt.synthesizer.utils.to_rtl`

The serialization process is usually a destructive operation as parts of AST can be rewritten
to fit target language.
"""
