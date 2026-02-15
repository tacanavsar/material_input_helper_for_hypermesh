# material_input_helper_for_hypermesh
This code help filling material entitites in hypermesh. Code utlises a csv file with the material data which can be exported from excel.
The csv file should be in the working directory of the hypermesh session.
You need to run the code inside hypermesh, after you open the model since it works only in the current model.
Currently the program is specific to filling out MAT8 entities.
The CSV file should be named "material_data.csv", it is the static name used inside the code.
