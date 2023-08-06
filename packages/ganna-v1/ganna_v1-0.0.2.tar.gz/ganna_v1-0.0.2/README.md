# Generative Algorithm for N-Doped Novel Aromatics

This algorithm can be used to generate nitrogen-doped polycyclic aromatic compounds whose geometry is optimised using the MMFF94s force field. The application of this algorithm is very straightforward to understand. The users are required to create a folder with the aromatic structures that they want to be doped with nitrogen atoms, specify the number of nitrogen atoms that they want in the structure, and provide the folder on which the MMFF94s optimised structures should be saved.  Please contact the author via email with any questions or concerns about the code (stiv.llenga@h-its.org).

## Setting the input variables:

Since the purpose of the algorithm is for everybody to use it, the amount of input needed to make it function properly is kept to a minimum. Users are required to provide the following information: 

INPUT:
   
* --inp_dir -> (Str) The directory that houses all of the PAH xyz files;
   
* --out_dir -> (Str) The directory where the N-doped PAH must be saved;
   
* --hetero_nr -> (Int) The total amount of dopants (Nitrogen atoms);

* --iters -> (Int) The maximum iteration value of the force field.
