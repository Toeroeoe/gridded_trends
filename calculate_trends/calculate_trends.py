
from timeit import default_timer as timer

from blitzcomp.parallel import pixel_wise
import data_config, custom_funcs
from argparse import ArgumentParser
import ast


if __name__ == '__main__':
    
    parser = ArgumentParser()
    
    parser.add_argument('--data', 
                        '-d', 
                        help = 'name of data dictionary', 
                        type = str)

    parser.add_argument('--variables', 
                        '-v', 
                        help = 'list of variable names',
                        nargs = '*', 
                        type = str)
    
    parser.add_argument('--year_start', 
                        '-y0', 
                        help = 'start year', 
                        type = int)
    
    parser.add_argument('--year_end', 
                        '-y1', 
                        help = 'end year', 
                        type = int)
    
    parser.add_argument('--month_start', 
                        '-m0', 
                        help = 'start month', 
                        type = int)
    
    parser.add_argument('--month_end', 
                        '-m1', 
                        help = 'end month', 
                        type = int)

    parser.add_argument('--slope_units', 
                        '-u', 
                        help = 'the resulting units of the trend', 
                        type = str)
    
    parser.add_argument('--outfile', 
                        '-o', 
                        help = 'path of the output file', 
                        type = str)
    
    parser.add_argument('--func_name',
                        '-fn',
                        help = 'custom function name',
                        type = str,
                        default = 'mankendall')
    
    parser.add_argument('--func_args',
                        '-fa',
                        help = 'arguments for custom function',
                        type = str)
    
    parser.add_argument('--delete_dims',
                        '-dd',
                        help = 'which dimensions to delete',
                        type = str)
    
    args = parser.parse_args()

    func_args = ast.literal_eval(args.func_args)

    units = ast.literal_eval(args.slope_units)

    delete_dims = ast.literal_eval(args.slope_units)

    start = timer()

    data_dict = getattr(data_config, args.data)

    vars_out = [f'{v}_slope' for v in args.variables] + \
               [f'{v}_p' for v in args.variables] + \
               [f'{v}_intercept' for v in args.variables]
    
    
    func = getattr(custom_funcs, args.func_name)

    pixel_wise(func,
               variables = args.variables,
               data = data_dict,
               variables_out = vars_out,
               units = units,
               file_out = args.outfile,
               return_shape = 0,
               return_dims = [],
               year_start = args.year_start,
               year_end = args.year_end,
               month_start = args.month_start,
               month_end = args.month_end,
               dtype = 'float64',
               **func_args)

    end = timer()

    print('\nParallel trend calculation done.\n')
    print(f'\nTime elapsed: {end - start} seconds.')




