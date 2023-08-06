"""Console script for wasabi S3."""
import sys
import click
from formatter import indicators



def initialize():
    accessKey = input(
        f"{indicators.OKCYAN}Enter your Access Key ID: {indicators.ENDC}"
    ).strip()
    secretAccessKey = input(
        f"{indicators.OKCYAN}Enter your Secret Access Key: {indicators.ENDC}"
    ).strip()
    bucketName = input(
        f"{indicators.OKCYAN}Enter your Bucket Name: {indicators.ENDC}"
    ).strip()
    endpoint = input(
        f"{indicators.OKCYAN}Specify the endpoint URL: {indicators.ENDC}"
    ).strip()

    WasabiClient = WasabiPurge(accessKey, secretAccessKey, endpoint, bucketName)

    return WasabiClient





class ScriptRunner:

    def __init__(self):
        pass

    def start(self):

        WasabiClient = initialize()

        print(
            f"{indicators.OKGREEN}Choose from the following list of operations to run on your Wasabi bucket: {WasabiClient.bucketName}"
        )
        print(
            f"\t{indicators.OKMAGENTA}Operation 1: Delete Non-Current Objects {indicators.ENDC}"
        )
        print(
            f"\t{indicators.OKMAGENTA}Operation 2: Delete Current and Non-Current Objects {indicators.ENDC}"
        )
        print(
            f"\t{indicators.OKMAGENTA}Operation 3: Purge Delete Markers {indicators.ENDC}"
        )
        print(f"\t{indicators.OKMAGENTA}Operation 4: Delete Bucket {indicators.ENDC}")

        acceptableOptions = [1, 2, 3, 4]
        userSelection = int(
            input(
                f"{indicators.WARNING}Select Operation (Number 1-4) : {indicators.ENDC}"
            ).strip()
        )

        if userSelection not in acceptableOptions:
            print(f"{indicators.FAIL}Wrong Option Selected :( Try again!{indicators.ENDC}")
        else:
            if userSelection == 1:
                WasabiClient.deleteNonCurrentsV2()
            elif userSelection == 2:
                for i in range(4):
                    WasabiClient.deleteVersionsandObjects()
            elif userSelection == 3:
                WasabiClient.purgeDeleteMarkers()
            elif userSelection == 4:
                WasabiClient.deleteBucket()


@click.command()
def main(args=None):
    """Console script for wasabi S3."""
    click.echo(f"{indicators.WARNING}Welcome to the Wasabi S3 CLI Tool{indicators.ENDC}")
    click.echo(f"{indicators.WARNING}--------------------------------------------------------{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@author: M. Salim Dason{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@version: 0.1.4{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@licence: GNU GENERAL PUBLIC LICENSE{indicators.ENDC}")
    click.echo(f"{indicators.FAIL}Note: Tool specifically designed for versioned buckets!{indicators.ENDC}")
    click.echo(f"{indicators.WARNING}---------------------------------------------------------{indicators.ENDC}\n")

    ScriptRunner().start()


if __name__ == "__main__":
    # main()
    sys.exit(main())
