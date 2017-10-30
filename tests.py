from __future__ import print_function
import os
import sys
import filecmp
import shutil



def run_tests():

    tests_descriptions = [
        "TESTING TRANSFORMATION OF SPECFILE TO SPECFILE CLASS JSON REPRESENTATION",
        "TESTING TRANSFORMATION OF SPECFILE CLASS TO SPECFILE",
        "TESTING TRANSFORMATION OF JSON INPUT TO SPECFILE",
        "TESTING TRANSFORMATION OF SPECFILE CLASS TO PRETTY PRINTED SPECFILE",
        "TESTING TRANSFORMATION OF SPECFILE TO SPECFILE CLASS 2.0 JSON REPRESENTATION",
        "TESTING TRANSFORMATION OF SPECFILE 2.0 to SPECFILE 1.0",
        "TESTING TRANSFORMATION OF SPECFILE TO GO SPECFILE YAML REPRESENTATION",
        "TESTING TRANSFORMATION OF GO SPECFILE TO SPECFILE 2.0 JSON REPRESENTATION"
    ]

    arguments = [
        '-j 1 -s 0 -p 0 -m 1',
        '-j 0 -s 1 -p 0 -m 1',
        '-j 0 -s 1 -p 0 -m 1',
        '-j 0 -s 1 -p 1 -m 1',
        '-j 1 -s 0 -p 0',
        '-j 0 -s 0 -p 0 --debug 1',
        '-j 1 -s 0 -p 0 -g 1',
        '-j 0 -s 0 -p 0 -g 1 -m 3 --debug 1'
    ]

    testing_specfiles = os.listdir(os.curdir + '/Tests/Inputs')
    failures = 0

    for test_number, testing_set in enumerate(arguments):
        output_filepath = './Tests/Outputs/' + str(test_number)
        if os.path.exists(output_filepath):
            shutil.rmtree(output_filepath)
        os.makedirs(output_filepath)

        print('\n' + tests_descriptions[test_number] + '\n')

        for index, specfile_filename in enumerate(testing_specfiles):

            if test_number == 2:
                source_file_path = ' -i ./Tests/RefOutputs/0/'
            else:
                source_file_path = ' -i ./Tests/Inputs/'

            os.system('python specparser_main.py ' + testing_set + source_file_path + specfile_filename + ' > ./Tests/Outputs/' + str(test_number) + '/' + specfile_filename)

            intro = 'TEST ' + str(index + 1) + ': '

            if test_number in [0, 3, 4, 6]:
                reference_output_path = './Tests/RefOutputs/' + str(test_number) + '/' + specfile_filename
            elif test_number == 5:
                reference_output_path = './Tests/RefOutputs/0/' + specfile_filename
            elif test_number == 7:
                reference_output_path = './Tests/RefOutputs/4/' + specfile_filename
            else:
                reference_output_path = './Tests/Inputs/' + specfile_filename

            if filecmp.cmp('./Tests/Outputs/' + str(test_number) + '/' + specfile_filename, reference_output_path, False):
                sys.stdout.write(intro + "\033[0;32m" + "SUCCESS!\n" + "\033[0;0m")
            else:
                sys.stdout.write(intro + "\033[1;31m" + "FAIL!" + "\033[0;0m" + " (" + specfile_filename + ")\n")
                failures += 1

    print('\nAll tests checked, totalling ' + str(failures) + ' errors!')

    return
