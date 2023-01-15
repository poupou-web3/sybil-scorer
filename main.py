# This scipts takes in imput a csv file with the list of address to score see an example of file in input folder the list can be non unique
# the script generates a csv file in Output folder with a column with the address and a column with

if __name__ == "__main__":

    import argparse
    scan_argparse = argparse.ArgumentParser()
    scan_argparse.description = "need input: -c chain_name -i input_file -t task -k flipside_api_key"

    scan_argparse.add_argument(
        "-c",
        "--chain",
        help=
        "the chain to scan ig: eth_classic, it can also be several chains for example [eth_classic, eth_polygon]",
        type=str,
        dest="chain_name")
    scan_argparse.add_argument(
        "-i",
        "--inputfile",
        help="the file contains the address list to scan",
        type=str,
        dest="input_file")
    scan_argparse.add_argument("-t",
                               "--task",
                               help="name the task",
                               type=str,
                               dest="task")
    scan_argparse.add_argument("-k",
                               "--apiKey",
                               help="Flipside api key",
                               type=str,
                               dest="flipside_api_key")
    scan_argparse.add_argument(
        "-n",
        "--init",
        help=
        "Set to true by default, if set to false it will use the data already retrieved in data",
        type=str,
        dest="init")
    scan_argparse.add_argument(
        "-s",
        "--seed",
        help="The seed for kmean clustering, if empty the seed is random",
        type=str,
        dest="input_file")

    args = scan_argparse.parse_args()

    # scan = ScanFetcher(args.chain_name, args.task, args.batchid, args.totalbatch, args.input_file, args.union_file)
    # scan.init_settings(args.start_num)
    # scan.run_scan()

    print(args)
