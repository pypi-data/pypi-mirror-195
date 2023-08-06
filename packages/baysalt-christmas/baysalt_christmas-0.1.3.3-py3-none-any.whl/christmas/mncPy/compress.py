#!/usr/bin/env python

""" Compresses a given set of netcdf files in parallel. The compressed files will be saved with a prefix "cmpr_".
    After having checked the compressed files are ok, you can run the following linux command to OVERRIDE all of
    the original files with their compressed versions:
        rename "cmpr_" "" cmpr_*
"""

from __future__ import print_function
import os
import argparse
import xarray as xr
import numpy as np
from mpi4py import MPI
from common import get_file_paths, GlobalData

# pylint: disable=line-too-long, bad-whitespace, len-as-condition, invalid-name


def parse_args():
    # Parse the CLI arguments provided by the user
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-f', metavar='path', type=str, required=True, nargs='*',
                        help='path to hist file(s) to read. Multiple files and wild characters (*) accepted.')
    parser.add_argument('-x', metavar='excl', type=str, required=False,
                        help='(optional). File names that have the string provided after this flag'
                             ' will be discarded. ')
    parser.add_argument('-v', action='store_true', required=False, help='Verbose logging')
    return parser.parse_args()
# Parse the CLI arguments provided by the user
# parser = argparse.ArgumentParser(description=__doc__)
# parser.add_argument('-f', metavar='path', type=str, required=True, nargs='*',
#                     help='path to hist file(s) to read. Multiple files and wild characters (*) accepted.')
# parser.add_argument('-x', metavar='excl', type=str, required=False,
#                     help='(optional). File names that have the string provided after this flag'
#                          ' will be discarded. ')
# parser.add_argument('-v', action='store_true', required=False, help='Verbose logging')
# args = parser.parse_args()


class mnc_Py:
    def __init__(self, f_path, x_excl=None, v_log=False, o_path=None):
        self.f = f_path
        self.x = x_excl
        self.v = v_log
        self.comm = MPI.COMM_WORLD
        self.o = o_path

    def MPI_comm(self):
        # MPI comm
        return self.comm

    def compress_files(self):
        # sourcery skip: de-morgan, flip-comparison, for-append-to-extend, list-comprehension, remove-redundant-slice-index, remove-str-from-fstring, use-fstring-for-concatenation
        """ compresses a given set of netcdf files """

        # get the list of files to compress
        filePaths = get_file_paths(self.f, comm.Get_rank(), self.x, self.v)
    
        # by default, exclude files that are already compressed by this script
        filePaths = [filePath for filePath in filePaths if len(filePath.name)>5 and "cmpr_"!=filePath.name[0:5]]
    
        if comm.Get_rank()==0:
            print("compressing "+str(len(filePaths))+" files...")
        comm.Barrier()
    
        # determine files to be compressed by each proc
        nprocs = comm.Get_size()
        nfiles = len(filePaths)
        f_per_proc = int(np.ceil(float(nfiles)/nprocs))
        lfiles = []
        for i in range(comm.Get_rank()*f_per_proc, min(nfiles, (comm.Get_rank()+1)*f_per_proc)):
            lfiles.append(filePaths[i])

        #  compress the files:
        compr_dict = dict(zlib=True, complevel=1)
        compr_dict['_FillValue'] = None
        for lfile in lfiles:
    
            path_in = os.path.join(lfile.base, lfile.name)
            if self.o is None:
                path_out = os.path.join(lfile.base, "cmpr_"+lfile.name)
            else:
                path_out = os.path.join(lfile.base, lfile.name)
            write_mode = 'w'

            if self.v:
                print("rank:", comm.Get_rank(), "\tcompressing", lfile.name, "(", lfiles.index(lfile)+1, "of", len(lfiles), ")")

            # get time dimension
            glob = GlobalData()
            glob.get_time_var_names(path_in, bound_required=False)
    
            # first, write the the coordinates
            with xr.open_dataset(path_in, decode_times=False, cache=False, decode_cf=False) as lfile_ds_in:
                with xr.Dataset(coords=lfile_ds_in.coords, attrs=lfile_ds_in.attrs) as lfile_ds_out:
                    var_list = lfile_ds_in.variables
                    if len(lfile_ds_in.coords)>0:
                        for var in lfile_ds_in.coords:
                            lfile_ds_out[var] = lfile_ds_in[var]
    
                        encoding_dict = {var: compr_dict for var in lfile_ds_in.coords}
                        lfile_ds_out.to_netcdf(path=path_out, mode=write_mode, unlimited_dims=[glob.time_str], encoding=encoding_dict)
                        write_mode = 'a'
    
            # now, write the remaining data arrays (one by one to eliminate memory limitation)
            for da in var_list:
                with xr.open_dataset(path_in, decode_times=False, cache=False, decode_cf=False) as lfile_ds_in:
                    with xr.Dataset(coords=lfile_ds_in.coords, attrs=lfile_ds_in.attrs) as lfile_ds_out:
                        if not da in lfile_ds_in.coords:
                            lfile_ds_out[da] = lfile_ds_in[da]
                            lfile_ds_out.to_netcdf(path=path_out, mode=write_mode, unlimited_dims=[glob.time_str], encoding={da: compr_dict})
                            write_mode = 'a'
    
        comm.Barrier()
        if comm.Get_rank()==0:
            print("done.")
        return comm


if __name__ == "__main__":
    args = parse_args()
    mnc = mnc_Py(args.f, args.x, args.v)
    comm = mnc.MPI_comm()
    if comm.Get_rank()==0:
        print(f"running with {str(comm.Get_size())} processors...")
    mnc.compress_files()
