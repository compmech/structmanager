rm -rf Apps*
rm -rf LX*
export INTEL_INSTALL_DIR=/nfs/cae/Ferramentas/EXEC/INTEL/v2011.5.220
/nfs/cae/Ferramentas/EXEC/MSC/sdk_2013/Tools/scons "$@"
