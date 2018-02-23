from __future__ import print_function
import sys
import json
import argparse
import ruamel.yaml

from tests import run_tests
from examples import run_examples
from model_methods import ModelMethods
from spec_model_generator import SpecModelGenerator
from go_spec_model_generator import GoSpecModelGenerator
from spec_transformator import SpecModelTransformator



def parse_arguments():
    """processes given arguments and stores requested options"""

    arg_parser = argparse.ArgumentParser() #description="TODO")

    arg_parser.add_argument('-i', '--input', dest='input', type=str,
                            help="path to input specfile")

    arg_parser.add_argument('-t', '--test', dest='test', type=int, choices=[0, 1], default=0,
                            help="turns on/off (1/0) tests run")

    arg_parser.add_argument('-j', '--json', dest='json', type=int, choices=[0, 1], default=0,
                            help="turns on/off (1/0) output in json")

    arg_parser.add_argument('-s', '--specfile', dest='specfile', type=int, choices=[0, 1], default=0,
                            help="turns on/off (1/0) output as a specfile")

    arg_parser.add_argument('-r', '--reduced', dest='reduced', type=int, choices=[0, 1], default=1,
                            help="turns on/off (1/0) reduced output in json, outputs only non-empty fields")

    arg_parser.add_argument('-c', '--config', dest='config', type=str,
                            help="path to configuration file")

    arg_parser.add_argument('-p', '--pretty-print', dest='pretty', type=int, choices=[0, 1], default=0,
                            help="output specfile in a normalized form")

    arg_parser.add_argument('-m', '--model', dest='model', type=int, choices=[1, 2, 3], default=2,
                            help="choose between specfile 1.0 and 2.0 abstract models")

    arg_parser.add_argument('--debug', dest='debug', type=int, choices=[0, 1], default=0,
                            help="for testing and debugging purposes")

    arg_parser.add_argument('-g', '--go_spec', dest='go_spec', type=int, choices=[0, 1], default=0,
                            help="for testing and debugging purposes only, transforms specfile into go specfile")

    arg_parser.add_argument('-e', '--examples', dest='examples', type=int, choices=[0, 1], default=0,
                            help="runs all available examples")

    return arg_parser.parse_args()



def process_args(args):

    specModelGenerator = SpecModelGenerator()
    goSpecModelGenerator = GoSpecModelGenerator()
    modelMethods = ModelMethods()

    # args.test == 1 => run all available tests
    if args.test:
        run_tests()
        sys.exit(0)

    # args.examples == 1 => run all available examples
    if args.examples:
        run_examples()
        sys.exit(0)

    # args.input is set => read and process input specfile or json file
    if args.input:
        specpath = args.input
    # args.input is not set => get specfile (or json file) location and read and process it
    else:
        specpath = None

    specModel = modelMethods.create_abstract_model(specpath)

    # args.specfile is set => read and process input specfile, write output as a specfile
    if args.specfile:
        # TODO
        modelMethods.class_to_specfile(specModel, args.pretty)

    # args.model is set to 1 and args.json is set => read and process input specfile, output specmodel in json
    if args.model and args.model == 1 and args.json:
        modelMethods.print_json_representation(specModel, args.reduced)
        print(json.dumps(specModel, default=lambda o: o.__dict__, sort_keys=True))

        # args.config is set => apply changes from given configuration file on specfile
        if args.config:
            modelMethods.process_config_file(specModel, args.config)

    # specModel = specModelGenerator.create_specmodel(specModel)
    # specTransformator = SpecModelTransformator(specModel)

    if args.go_spec:
        # TODO
        goSpecModelGenerator.create_go_spec_model(json.dumps(modelMethods.remove_empty_fields(specModel), default=lambda o: o.__dict__, sort_keys=True))

        # print(json.dumps(GoSpecfile, default=lambda o: o.__dict__, sort_keys=True) + "\n\n")
        # print(ruamel.yaml.dump(ruamel.yaml.safe_load(json.dumps(reduce_gospecmodel(), default=lambda o: o.__dict__, sort_keys=True))))
        
        if args.json:
            print(ruamel.yaml.round_trip_dump(ruamel.yaml.safe_load(
                json.dumps(goSpecModelGenerator.reduce_gospecmodel(), default=lambda o: o.__dict__, sort_keys=True)),
                                              default_flow_style=False, indent=4,
                                              block_seq_indent=2, width=80))

    # args.debug is set => read and process input specfile, transform into gospec model and then back to specmodel
    if args.debug and args.model == 3:
        # TODO
        specmodel_from_gospec = goSpecModelGenerator.transform_gospec_to_specmodel(json.dumps(goSpecModelGenerator.gospecmodel, default=lambda o: o.__dict__, sort_keys=True))
        print(json.dumps(modelMethods.remove_empty_fields(json.loads(specmodel_from_gospec)), default=lambda o: o.__dict__, sort_keys=True))



def main():
    """MAIN"""

    args = parse_arguments()

    process_args(args)

    return 0



if __name__ == "__main__":
    main()
